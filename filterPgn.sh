StartsWith=$1
FileID=$2

cat tmp/output-$FileID.json | jq '.[] | select(.PGN | startswith("'$StartsWith'"))' | jq -s > tmp/output-$FileID-prop.json