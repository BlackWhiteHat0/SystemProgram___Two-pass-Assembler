#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./compile_show_execute.sh <filename.s>"
    exit 1
fi

INPUT_FILE="$1"

# 處理檔案路徑，如果直接給檔名且當下沒有，嘗試加上 Demo/
if [ ! -f "$INPUT_FILE" ]; then
    if [ -f "Demo/$INPUT_FILE" ]; then
        INPUT_FILE="Demo/$INPUT_FILE"
    else
        echo "Error: File '$INPUT_FILE' not found."
        exit 1
    fi
fi

echo "===== 1. Compiling ====="
python3 compiler.py "$INPUT_FILE"
if [ $? -ne 0 ]; then
    echo "Compilation failed."
    exit 1
fi

# 將檔名的 .s 替換為 .obj0
OBJ_FILE="${INPUT_FILE%.s}.obj0"

echo ""
echo "===== 2. Hex Dump ($OBJ_FILE) ====="
xxd "$OBJ_FILE"

echo ""
echo "===== 3. Executing with vm0 ====="
./vm0 "$OBJ_FILE"
