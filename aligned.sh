#!/bin/bash

# 設定輸入與輸出資料夾
INPUT_DIR="TestData"
OUTPUT_DIR="Results"

mkdir -p "$OUTPUT_DIR"

# 遍歷 TestData 裡的 .faa 檔案
for file_path in "$INPUT_DIR"/*.faa; do
    
    # 檢查檔案是否存在
    [ -e "$file_path" ] || continue

    # 取得檔案名稱（不含路徑）
    filename=$(basename "$file_path")

    # 設定輸出路徑
    output_path="$OUTPUT_DIR/mu_$filename"

    echo "正在使用 MAFFT 處理: $file_path"
    
    # MAFFT 標準語法：mafft [options] input > output
    # --auto 會根據序列大小自動選擇最適當的演算法
    mafft --auto "$file_path" > "$output_path"

done

echo "MAFFT 批次處理完成！"
