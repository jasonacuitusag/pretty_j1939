FILENAME=48476bf1-f33d-4060-9d7f-a31e92e1d38a

INPUT_FILENAME="tmp/$FILENAME"
OUTPUT_FILENAME="tmp/output-$FILENAME.json"

rm -rf "$OUTPUT_FILENAME"

python3 pretty_j1939.py --input-separator ',' --timestamp-column 0 --format --link --include-na --transport --da-json J1939DA_MAY2022.json "$INPUT_FILENAME" > "$OUTPUT_FILENAME"
# python3 pretty_j1939.py --input-separator ',' --timestamp-column 0 --format --candata                       --da-json J1939DA_MAY2022.json "$INPUT_FILENAME" > "$OUTPUT_FILENAME"
