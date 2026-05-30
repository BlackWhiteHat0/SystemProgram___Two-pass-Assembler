import sys
import os
from Assembler import CPU0Assembler

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 compiler.py <input_file.s>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
        
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading file '{input_file}': {e}")
        sys.exit(1)
        
    print(f"正在組譯: {input_file}...")
    
    try:
        assembler = CPU0Assembler()
        obj_data = assembler.assemble(code)
    except Exception as e:
        print(f"組譯失敗: {e}")
        sys.exit(1)
        
    # Determine the output filename (replace extension with .obj0)
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}.obj0"
    
    try:
        with open(output_file, "wb") as f:
            f.write(obj_data)
        print(f"已輸出: {output_file} (共 {len(obj_data)} bytes)")
    except Exception as e:
        print(f"Error writing to file '{output_file}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
