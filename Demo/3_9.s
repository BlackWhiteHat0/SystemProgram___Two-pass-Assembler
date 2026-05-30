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
