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
