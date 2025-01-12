# 💻 PTX IR Visualizer

## 🚀 Overview
**PTX IR Visualizer** is a tool that helps **GPU developers** compare different versions of **PTX (Parallel Thread Execution)** code. It highlights the **changes, optimizations, or regressions** between two PTX files, providing both a **Command-Line Interface (CLI)** and a **Matrix-style Web GUI**.

This tool enables **CUDA developers** and **compiler engineers** to see **how their high-level code transforms into GPU assembly**, making it easier to catch **performance regressions** or **track optimizations**.

---

## ✨ Features
- 🖥️ **Command-Line Interface (CLI) Tool**
- 🌐 **Web-Based GUI with Matrix Theme**
- 🔍 **Textual Diff of PTX Code Changes**
- 📈 **Graph Rendering of Instruction Flows (Basic)**
- 🟢 **Color-Coded Differences (Green for Added, Red for Removed)**

---

## 📋 How It Works
1. **Input two PTX files (Version A and Version B).**
2. **The tool parses both files, compares kernel instructions, and shows:**
   - Added/Removed instructions.
   - New/Removed kernels.
   - Resource usage differences.
3. **View the results in:**
   - **Command Line** for quick comparisons.
   - **Web GUI** with a **Matrix-style aesthetic**.

---

## 🛠️ How to Use

### 1️⃣ Run the Web App

flask run --host=0.0.0.0 --port=8000

Open your browser and go to:

http://127.0.0.1:8000

### 2️⃣ Run the CLI Tool

python run_visualizer.py --ptx_files sample_ptx/version_a.ptx sample_ptx/version_b.ptx

### 🧪 Test Inputs

Use the following sample inputs to test the tool:

PTX Version A:

.visible .entry myKernel() {
    mov.b32 %r1, %r2;
    ld.param.u32 %r3, [_Z6param_0];
}

PTX Version B:

.visible .entry myKernel() {
    mov.b32 %r1, %r2;
    ld.global.u32 %r3, [%rd1];
}

### 📊 Expected Output

Command Line:

Comparing kernel: myKernel
Changes in myKernel:
--- PTX_A
+++ PTX_B
@@ -1,2 +1,2 @@
 mov.b32 %r1, %r2
-ld.param.u32 %r3, [_Z6param_0]
+ld.global.u32 %r3, [%rd1]

### Web GUI:

A Matrix-style interface showing:

🟢 Added lines in green.

🔴 Removed lines in red.

⚪ Unchanged lines in grey.
