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
