#!/bin/bash

INPUT_DIR="TestData"
OUTPUT_DIR="Results"

mkdir -p "$OUTPUT_DIR"

for file_path in "$INPUT_DIR"/*.faa; do
    
    [ -e "$file_path" ] || continue

    filename=$(basename "$file_path")

    output_path="$OUTPUT_DIR/mu_$filename"

    echo "Processing with MAFFT...: $file_path"
    
    mafft --auto "$file_path" > "$output_path"

done

echo "MAFFT batch processing complete！"

