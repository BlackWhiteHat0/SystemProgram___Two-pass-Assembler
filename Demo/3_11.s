        LD R2, x
        CALL f
        ST R1, y
        RET
    x:  WORD 1
    y:  RESW 1
    f:  
        ADD R1, R2, R2
        RET
