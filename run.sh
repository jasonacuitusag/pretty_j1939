FILENAME=hump-chain-speed-1

INPUT_FILENAME="tmp/$FILENAME.txt"
OUTPUT_FILENAME="tmp/output-$FILENAME.json"

python3 pretty_j1939.py  --format --link --include-na --transport --da-json J1939DA_MAY2022.json tmp/$FILENAME.txt > tmp/output-$FILENAME.json
#python3 pretty_j1939.py  --format --da-json J1939DA_MAY2022.json --candata "$INPUT_FILENAME" > "$OUTPUT_FILENAME"
