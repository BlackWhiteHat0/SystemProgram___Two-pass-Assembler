# CPU0 Two-pass Assembler 專案說明文件

本專案實作了一個針對 CPU0 指令集的兩階段組譯器（Two-pass Assembler），並提供了編譯與模擬執行的工具鏈。

## 檔案與目錄說明

### 核心組件
*   **`Assembler.py`**: 
    *   **核心組譯邏輯**。
    *   實作了兩階段組譯過程：第一階段建立符號表（Symbol Table），第二階段生成機器碼。它負責處理指令轉換、記憶體配置（RESB/RESW）以及資料定義（BYTE/WORD）。
*   **`vm0`**: 
    *   **CPU0 虛擬機（執行檔）**。
    *   負責讀取 `.obj0` 二進位機器碼檔案並在虛擬的 CPU 環境中執行，最後會印出暫存器（Registers）與記憶體（Memory）的狀態。

### 工具腳本
*   **`compiler.py`**: 
    *   **命令列編譯工具**。
    *   這是一個 Python 腳本，封裝了 `Assembler.py` 的功能。
    *   用法：`python3 compiler.py <path_to_asm>.s`
    *   功能：讀取組譯原始碼，輸出生產的二進位機器碼檔 (`.obj0`)。
*   **`compile_show_execute.sh`** (Linux) / **`compile_show_execute.bat`** (Windows):
    *   **一鍵自動化腳本**。
    *   這是一個整合性的自動化工具，執行過程包含：
        1.  呼叫 `compiler.py` 進行組譯。
        2.  使用 `xxd` 顯示生成的 `.obj0` 檔的十六進位內容（Hex Dump）。
        3.  呼叫 `./vm0` 執行編譯後的程式。
    *   用法：`./compile_show_execute.sh <filename>.s`

### 範例與資料
*   **`Demo/`**: 
    *   **範例程式資料夾**。
    *   存放所有的組譯原始碼檔案 (`.s`) 以及編譯後的結果 (`.obj0`)。
    *   包含範例：`3_8.s`, `3_9.s`, `3_11.s`, `3_12.s`。
*   **`main.py`**: 
    *   原先的測試進入點，包含了內嵌的範例程式碼，用於快速驗證組譯器的正確性。

## 使用流程範例

如果你想要編譯並執行 `Demo` 資料夾下的範例，最快的方法是使用自動化腳本：

```bash
# 賦予執行權限 (僅 Linux 需要一次性操作)
chmod +x compile_show_execute.sh

# 執行範例 3_8
./compile_show_execute.sh 3_8.s
```

這將會依序顯示組譯結果、十六進位碼，以及虛擬機執行後的暫存器 dump。
