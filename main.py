from Assembler import CPU0Assembler


# ==========================================
# Demo 驗證區 (編譯 4 個範例並輸出 obj0)
# ==========================================
EXAMPLES = {
    "3_8": """
        LD R1, i
        LD R2, aptr
        LD R3, bptr
        LDI R7, 1
    while:
        LDB R4, [R3]
        STB R4, [R2]
        ADD R2, R2, R7
        ADD R3, R3, R7
        CMP R4, R0
        JEQ endw
        JMP while
    endw:
        RET
    a:      RESB 10
    b:      BYTE "Hello !", 0
    i:      WORD 0
    aptr:   WORD a
    bptr:   WORD b
    """,
    "3_9": """
        LD R1, i
        LD R2, aptr
        LD R3, bptr
        LDI R7, 1
    while:
        LBR R4, [R3+R1]
        SBR R4, [R2+R1]
        CMP R4, R0
        JEQ endw
        ADD R1, R1, R7
        JMP while
    endw:   RET
    a:      RESB 10
    b:      BYTE "Hello !", 0
    aptr:   WORD a
    bptr:   WORD b
    i:      WORD 0
    """,
    "3_11": """
        LD R2, x
        CALL f
        ST R1, y
        RET
    x:  WORD 1
    y:  RESW 1
    f:  
        ADD R1, R2, R2
        RET
    """,
    "3_12": """
        LD R2, x
        PUSH R2
        CALL f1
        ST R1, y
        RET
    x:  WORD 1
    y:  RESW 1
    f1:
        POP R2
        PUSH LR
        ST R2, t
        LD R3, pt
        PUSH R3
        CALL f2
        ST R1, b
        ADD R1, R1, R1
        POP LR
        RET
    t:  RESW 1
    b:  RESW 1
    pt: WORD t
    f2:
        POP R2
        LD R3, [R2]
        LDI R4, 5
        ADD R1, R3, R4
        ST R1, r
        RET
    r:  RESW 1
    """
}

if __name__ == "__main__":
    for name, code in EXAMPLES.items():
        print(f"正在組譯範例 {name}...")
        assembler = CPU0Assembler()
        obj_data = assembler.assemble(code)
        
        # 寫入二進位檔案
        filename = f"demo_{name}.obj0"
        with open(filename, "wb") as f:
            f.write(obj_data)
        
        print(f"已輸出: {filename} (共 {len(obj_data)} bytes)\n")
