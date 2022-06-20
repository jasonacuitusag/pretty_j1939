#!/usr/bin/env python3

import bitstring
import argparse
import sys
import json
import importlib

import pretty_j1939.describe

defaults = importlib.import_module('arg_defaults').defaults if importlib.util.find_spec("arg_defaults") else {}

def put_if_absent(key, value):
    if key not in defaults:
        defaults[key] = value

put_if_absent('da-json',    pretty_j1939.describe.DEFAULT_DA_JSON)
put_if_absent('candata',    pretty_j1939.describe.DEFAULT_CANDATA)
put_if_absent('pgn',        pretty_j1939.describe.DEFAULT_PGN)
put_if_absent('spn',        pretty_j1939.describe.DEFAULT_SPN)
put_if_absent('transport',  pretty_j1939.describe.DEFAULT_TRANSPORT)
put_if_absent('link',       pretty_j1939.describe.DEFAULT_LINK)
put_if_absent('include_na', pretty_j1939.describe.DEFAULT_INCLUDE_NA)
put_if_absent('real-time',  pretty_j1939.describe.DEFAULT_REAL_TIME)

put_if_absent('format',           False)
put_if_absent('input-separator',  None)
put_if_absent('pgn-column',       1)
put_if_absent('pgn-data-column', -1)
put_if_absent('timestamp-column', None)
put_if_absent('json-array',       False)


parser = argparse.ArgumentParser(description='pretty-printing J1939 candump logs')
parser.add_argument('candump', help='candump log, use - for stdin')

parser.add_argument('--da-json', type=str, const=True, default=defaults['da-json'], nargs='?',
                    help='absolute path to the input JSON DA (default=\"./J1939db.json\")')

parser.add_argument('--candata',    dest='candata', action='store_true',  help='print input can data')
parser.add_argument('--no-candata', dest='candata', action='store_false', help='(default)')
parser.set_defaults(candata=defaults['candata'])

parser.add_argument('--pgn',    dest='pgn', action='store_true', help='(default) print source/destination/type '
                                                                      'description')
parser.add_argument('--no-pgn', dest='pgn', action='store_false')
parser.set_defaults(pgn=defaults['pgn'])

parser.add_argument('--spn',    dest='spn', action='store_true', help='(default) print signals description')
parser.add_argument('--no-spn', dest='spn', action='store_false')
parser.set_defaults(spn=defaults['spn'])

parser.add_argument('--transport',    dest='transport', action='store_true',  help='print details of transport-layer '
                                                                                   'streams found (default)')
parser.add_argument('--no-transport', dest='transport', action='store_false', help='')
parser.set_defaults(transport=defaults['transport'])

parser.add_argument('--link',    dest='link', action='store_true',  help='print details of link-layer frames found')
parser.add_argument('--no-link', dest='link', action='store_false', help='(default)')
parser.set_defaults(link=defaults['link'])

parser.add_argument('--include-na',    dest='include_na', action='store_true',  help='include not-available (0xff) SPN '
                                                                                     'values')
parser.add_argument('--no-include-na', dest='include_na', action='store_false', help='(default)')
parser.set_defaults(include_na=defaults['include_na'])

parser.add_argument('--real-time',    dest='real_time', action='store_true',  help='emit SPNs as they are seen in '
                                                                                   'transport sessions')
parser.add_argument('--no-real-time', dest='real_time', action='store_false', help='(default)')
parser.set_defaults(real_time=defaults['real-time'])

parser.add_argument('--format',    dest='format', action='store_true',  help='format each structure (otherwise '
                                                                             'single-line)')
parser.add_argument('--no-format', dest='format', action='store_false', help='(default)')
parser.set_defaults(format=defaults['format'])

parser.add_argument('--input-separator', type=str, const=True, default=defaults['input-separator'], nargs='?',
                    help='separator to use when splitting a line.')

parser.add_argument('--pgn-column', type=int, const=True, default=defaults['pgn-column'], nargs='?',
                    help='zero based index of the column containg the pgn code')

parser.add_argument('--pgn-data-column', type=int, const=True, default=defaults['pgn-data-column'], nargs='?',
                    help='zero based index of the column containg the pgn data')

parser.add_argument('--timestamp-column', type=int, const=True, default=defaults['timestamp-column'], nargs='?',
                    help='zero based index of the column containg a integer timestamp')

parser.add_argument('--json-array',    dest='json_array', action='store_true', help='output a json array')
parser.add_argument('--no-json-array', dest='json_array', action='store_false')
parser.set_defaults(json_array=defaults['json-array'])

args = parser.parse_args()

if args.pgn_data_column < 0:
    args.pgn_data_column = args.pgn_column + 1

if args.input_separator is None:
    line_parser = lambda candump_line: candump_line.strip().split()[2].split('#')
else:
    field_selector = lambda all_fields: [
        all_fields[args.pgn_column],
        all_fields[args.pgn_data_column],
        all_fields[args.timestamp_column if args.timestamp_column is not None else 0]]
    line_parser = lambda candump_line: field_selector(candump_line.strip().split(args.input_separator))

if args.json_array:
    print_header = lambda: print('[')
    print_line = lambda desc_line, is_first_line: print(desc_line, end = '') if is_first_line else print(',\n', desc_line, end = '', sep='')
    print_footer = lambda: print('\n]')
else:
    print_header = lambda: None
    print_line = lambda desc_line, _: print(desc_line)
    print_footer = lambda: None


def process_lines(candump_file):
    is_first_line = True
    print_header()

    for candump_line in candump_file.readlines():
        if candump_line == '\n':
            continue

        try:
            message = line_parser(candump_line)
            message_id = bitstring.ConstBitArray(hex=message[0])
            message_data = bitstring.ConstBitArray(hex=message[1])
        except (IndexError, ValueError):
            print("Warning: error in line '%s'" % candump_line, file=sys.stderr)
            continue

        desc_line = ''

        description = describe(message_data.bytes, message_id.uint)

        description["Hex Data"] = message[1]

        if args.timestamp_column is not None:
            description["Timestamp"] = message[2]
            description.move_to_end("Timestamp", last=False)
        if args.format:
            json_description = str(json.dumps(description, indent=4))
        else:
            json_description = str(json.dumps(description, separators=(',', ':')))
        if len(description) > 0:
            desc_line = desc_line + json_description

        if args.candata:
            can_line = candump_line.rstrip() + " ; "
            if not args.format:
                desc_line = can_line + desc_line
            else:
                formatted_lines = desc_line.splitlines()
                if len(formatted_lines) == 0:
                    desc_line = can_line
                else:
                    first_line = formatted_lines[0]
                    desc_line = can_line + first_line
                    formatted_lines.remove(first_line)

                for line in formatted_lines:
                    desc_line = desc_line + '\n' + ' ' * len(candump_line) + "; " + line

        if len(desc_line) > 0:
           print_line(desc_line, is_first_line)
           is_first_line = False

    print_footer()


if __name__ == '__main__':
    describe = pretty_j1939.describe.get_describer(
                                da_json=args.da_json,
                                describe_pgns=args.pgn,
                                describe_spns=args.spn,
                                describe_link_layer=args.link,
                                describe_transport_layer=args.transport,
                                real_time=args.real_time,
                                include_transport_rawdata=args.candata,
                                include_na=args.include_na)
    if args.candump == '-':
        f = sys.stdin
    else:
        f = open(args.candump, 'r')

    process_lines(f)
