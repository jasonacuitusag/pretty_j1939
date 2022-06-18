FILENAME=test_data

INPUT_FILENAME="tmp/$FILENAME"
OUTPUT_FILENAME="tmp/output-$FILENAME.json"

rm -rf "$OUTPUT_FILENAME"

python3 pretty_j1939.py --input-separator ',' --timestamp-column 0 --format --link --include-na --transport --da-json J1939DA_MAY2022.json "$INPUT_FILENAME" > "$OUTPUT_FILENAME"
# python3 pretty_j1939.py --input-separator ',' --timestamp-column 0 --format --candata                       --da-json J1939DA_MAY2022.json "$INPUT_FILENAME" > "$OUTPUT_FILENAME"
