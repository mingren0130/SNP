# 📘 README

## 📂 Project Overview
This project is designed to process genomic sequence data, including:
1. Raw sequence preparation  
2. Sequence alignment  
3. SNP generation  

---

## 📁 Directory Structure

project/
│
├── TestData/        # Raw sequence data
├── aligned/         # Aligned sequences (can be used directly)
├── aligned.sh       # Batch alignment script (uses MAFFT)
├── SNP.py           # SNP generation script
└── README.md

---

## ⚙️ Requirements

Please install MAFFT before running this project.

### Installation Examples

Linux / WSL:
sudo apt-get install mafft

Mac:
brew install mafft

---

## 🚀 Workflow

### 🔹 Step 1: Prepare Data
Place your raw sequence files in:

TestData/

---

### 🔹 Step 2: Sequence Alignment

There are two options:

#### ✅ Option 1: Use the script (Recommended)

bash aligned.sh

👉 This will automatically perform MAFFT alignment on files in TestData/  
👉 Output will be saved in aligned/  

---

#### ✅ Option 2: Use pre-aligned data

You can directly use the files inside:

aligned/

---

### 🔹 Step 3: Generate SNP Data

Run the SNP script:

python SNP.py

👉 This will convert files in aligned/ into SNP format  

---

## 📌 Notes

- The aligned/ folder is the main input for downstream analysis  
- For large datasets, it is recommended to complete alignment first  
- aligned.sh requires MAFFT to function properly  

---

## 🧠 Pipeline Overview

TestData (raw data)
        ↓
MAFFT (aligned.sh)
        ↓
aligned (alignment results)
        ↓
SNP.py
        ↓
SNP data
