import re

# 根據講義 as0 檔案內容，建立 CPU0 指令表與對應的格式 (L, A, J)
OPTABLE = {
    "LD":   {"op": 0x00, "type": "L"}, "ST":   {"op": 0x01, "type": "L"},
    "LDB":  {"op": 0x02, "type": "L"}, "STB":  {"op": 0x03, "type": "L"},
    "LDR":  {"op": 0x04, "type": "L"}, "STR":  {"op": 0x05, "type": "L"},
    "LBR":  {"op": 0x06, "type": "L"}, "SBR":  {"op": 0x07, "type": "L"},
    "LDI":  {"op": 0x08, "type": "L"},
    "CMP":  {"op": 0x10, "type": "A"}, "MOV":  {"op": 0x12, "type": "A"},
    "ADD":  {"op": 0x13, "type": "A"}, "SUB":  {"op": 0x14, "type": "A"},
    "MUL":  {"op": 0x15, "type": "A"}, "DIV":  {"op": 0x16, "type": "A"},
    "AND":  {"op": 0x18, "type": "A"}, "OR":   {"op": 0x19, "type": "A"},
    "XOR":  {"op": 0x1A, "type": "A"},
    "ROL":  {"op": 0x1C, "type": "A"}, "ROR":  {"op": 0x1D, "type": "A"},
    "SHL":  {"op": 0x1E, "type": "A"}, "SHR":  {"op": 0x1F, "type": "A"},
    "JEQ":  {"op": 0x20, "type": "J"}, "JNE":  {"op": 0x21, "type": "J"},
    "JLT":  {"op": 0x22, "type": "J"}, "JGT":  {"op": 0x23, "type": "J"},
    "JLE":  {"op": 0x24, "type": "J"}, "JGE":  {"op": 0x25, "type": "J"},
    "JMP":  {"op": 0x26, "type": "J"},
    "SWI":  {"op": 0x2A, "type": "L"}, "CALL": {"op": 0x2B, "type": "J"},
    "RET":  {"op": 0x2C, "type": "J"},
    "PUSH": {"op": 0x30, "type": "J"}, "POP":  {"op": 0x31, "type": "J"},
    "PUSHB":{"op": 0x32, "type": "J"}, "POPB": {"op": 0x33, "type": "J"}
}

class CPU0Assembler:
    def __init__(self):
        self.symtab = {}       # 符號表 (Symbol Table)
        self.obj_code = bytearray() # 最終的目的碼
        self.pass1_lines = []  # 暫存 PASS1 的解析結果供 PASS2 使用

    # ==========================================
    # 第一階段 (PASS1)：計算位址、建立符號表
    # ==========================================
    def pass1(self, asm_code):
        pc = 0
        for line in asm_code.splitlines():
            # 清除註解與首尾空白
            orig_line = line
            line = line.split('//')[0].split(';')[0].strip()
            if not line: continue
            
            # 處理 Label
            label = None
            if ':' in line:
                parts = line.split(':', 1)
                label = parts[0].strip()
                line = parts[1].strip()
                if label:
                    if label in self.symtab:
                        raise ValueError(f"標記重複定義: {label}")
                    self.symtab[label] = pc
            
            if not line: continue
            
            # 取出 Opcode 與參數
            tokens = line.split(None, 1)
            op = tokens[0].upper()
            args_str = tokens[1].strip() if len(tokens) > 1 else ""
            
            self.pass1_lines.append((pc, op, args_str, orig_line))
            
            # 計算下一個位址 (對應講義 PASS1)
            if op == 'BYTE':
                pc += len(self.parse_byte_args(args_str))
            elif op == 'WORD':
                args = [a.strip() for a in args_str.split(',')]
                pc += 4 * len(args)
            elif op == 'RESW':
                pc += 4 * int(args_str)
            elif op == 'RESB':
                pc += int(args_str)
            elif op in OPTABLE:
                pc += 4
            else:
                raise ValueError(f"拼寫有誤或未知的指令: {op}")

    # ==========================================
    # 第二階段 (PASS2)：指令轉為機器碼
    # ==========================================
    def pass2(self):
        for pc, op, args_str, orig in self.pass1_lines:
            if op == 'BYTE':
                self.obj_code.extend(self.parse_byte_args(args_str))
            elif op == 'WORD':
                args = [a.strip() for a in args_str.split(',')]
                for arg in args:
                    val = self.symtab.get(arg, None)
                    if val is None:
                        val = int(arg, 0)
                    self.obj_code.extend(val.to_bytes(4, byteorder='big', signed=True))
            elif op == 'RESW':
                self.obj_code.extend(b'\x00' * (4 * int(args_str)))
            elif op == 'RESB':
                self.obj_code.extend(b'\x00' * int(args_str))
            elif op in OPTABLE:
                # 轉換為 32-bit (4 bytes) 機器碼
                code = self.translate_instruction(pc, op, args_str)
                self.obj_code.extend(code.to_bytes(4, byteorder='big', signed=False))

    # ==========================================
    # 指令轉換函數 (對應講義 TranslateInstruction)
    # ==========================================
    def translate_instruction(self, pc, op, args_str):
        op_info = OPTABLE[op]
        opcode = op_info['op']
        fmt = op_info['type']
        args = self.parse_operands(args_str)
        
        ra, rb, rc, cx = 0, 0, 0, 0
        
        def reg_id(r_str):
            if r_str == 'LR': return 14
            if r_str == 'SP': return 13
            if r_str == 'SW': return 12
            if r_str == 'PC': return 15
            return int(r_str.replace('R', ''))
        
        # 根據指令類型轉換 (L型, A型, J型)
        if fmt == 'L':
            if len(args) > 0:
                ra = reg_id(args[0][1])
                if len(args) > 1:
                    arg2 = args[1]
                    if arg2[0] == 'SYM':      # 變數 -> 位移 (標記 - PC)
                        rb = 15 # 預設使用 PC (R15)
                        cx = self.symtab[arg2[1]] - (pc + 4)
                    elif arg2[0] == 'IMM':    # 常數
                        rb = 0
                        cx = arg2[1]
                    elif arg2[0] == 'MEM_IMM': # [Rb] 或 [Rb+Cx]
                        rb = reg_id(arg2[1])
                        cx = int(arg2[2])
                    elif arg2[0] == 'MEM_REG': # [Rb+Rc] (例如 LBR R4, [R3+R1])
                        rb = reg_id(arg2[1])
                        rc = reg_id(arg2[2])
                        # 借用 Rc 欄位 (A型擴充編碼)
                        return (opcode << 24) | ((ra & 0xF) << 20) | ((rb & 0xF) << 16) | ((rc & 0xF) << 12)
            return (opcode << 24) | ((ra & 0xF) << 20) | ((rb & 0xF) << 16) | (cx & 0xFFFF)
            
        elif fmt == 'A':
            if len(args) > 0: ra = reg_id(args[0][1])
            if len(args) > 1: rb = reg_id(args[1][1])
            if len(args) > 2:
                arg3 = args[2]
                if arg3[0] == 'REG':
                    rc = reg_id(arg3[1])
                elif arg3[0] == 'IMM':
                    cx = arg3[1]
            return (opcode << 24) | ((ra & 0xF) << 20) | ((rb & 0xF) << 16) | ((rc & 0xF) << 12) | (cx & 0xFFF)
            
        elif fmt == 'J':
            if op in ['PUSH', 'POP', 'PUSHB', 'POPB']:
                if len(args) > 0: ra = reg_id(args[0][1])
                return (opcode << 24) | ((ra & 0xF) << 20)
            else:
                if len(args) > 0:
                    arg = args[0]
                    if arg[0] == 'SYM':
                        cx = self.symtab[arg[1]] - (pc + 4) # JMP 算 PC-relative
                    else:
                        cx = arg[1]
                return (opcode << 24) | (cx & 0xFFFFFF)
        return 0

    # -------- 輔助字串解析函數 --------
    def parse_byte_args(self, args_str):
        # 解析 BYTE "Hello !", 0 這種混合格式
        bytes_out = []
        in_str, curr_str, curr_num = False, "", ""
        for char in args_str:
            if char == '"':
                if in_str:
                    bytes_out.extend(curr_str.encode('ascii'))
                    curr_str, in_str = "", False
                else: in_str = True
            elif in_str: curr_str += char
            else:
                if char in ' ,':
                    if curr_num:
                        bytes_out.append(int(curr_num, 0) & 0xFF)
                        curr_num = ""
                else: curr_num += char
        if curr_num: bytes_out.append(int(curr_num, 0) & 0xFF)
        return bytes_out

    def parse_operands(self, args_str):
        # 拆解運算元 (處理暫存器、括號記憶體尋址)
        args, curr, in_bracket = [], "", False
        for char in args_str:
            if char == '[': in_bracket = True
            elif char == ']': in_bracket = False
            
            if char == ',' and not in_bracket:
                args.append(curr.strip())
                curr = ""
            else: curr += char
        if curr.strip(): args.append(curr.strip())
        
        parsed = []
        for arg in args:
            if arg.startswith('[') and arg.endswith(']'):
                inner = arg[1:-1]
                if '+' in inner:
                    left, right = inner.split('+')
                    parsed.append(('MEM_REG' if right.strip().startswith('R') else 'MEM_IMM', left.strip(), right.strip()))
                else: parsed.append(('MEM_IMM', inner.strip(), "0"))
            elif (arg.startswith('R') and arg[1:].isdigit()) or arg == 'LR':
                parsed.append(('REG', arg))
            elif arg.lstrip('-').isdigit(): parsed.append(('IMM', int(arg)))
            else: parsed.append(('SYM', arg))
        return parsed

    def assemble(self, asm_code):
        self.pass1(asm_code)
        self.pass2()
        return self.obj_code






