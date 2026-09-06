# 📘 README

## 📂 Project Overview

This project is designed to process genomic FASTA sequence data, including:

1. FASTA sequence preparation  
2. Sequence alignment  
3. SNP data generation  

---

## 📁 Directory Structure

```text
project/
│
├── TestData/        # Unaligned FASTA sequence files
├── aligned/         # Aligned sequences (can be used directly)
├── aligned.sh       # Batch alignment script (uses MAFFT)
├── SNP.py           # SNP generation script
└── README.md
```

---

## ⚙️ Requirements

Please install **Python 3** and **MAFFT** before running this project.

### Installation Examples

Linux / WSL:

```bash
sudo apt-get update
sudo apt-get install mafft
```

Mac:

```bash
brew install mafft
```

Check whether MAFFT and Python 3 are installed:

```bash
mafft --version
python3 --version
```

---

## 🚀 Workflow

### 🔹 Step 1: Prepare Data

Place your unaligned FASTA sequence files in:

```text
TestData/
```

> This pipeline uses FASTA files such as `.fa`, `.fasta`, or `.fna`. It does not directly process raw FASTQ sequencing reads.

---

### 🔹 Step 2: Sequence Alignment

There are two options:

#### ✅ Option 1: Use the Script (Recommended)

```bash
bash aligned.sh
```

👉 This automatically performs MAFFT alignment on the files in `TestData/`.  
👉 The alignment results are saved in `aligned/`.

#### ✅ Option 2: Use Pre-aligned Data

You can directly place and use pre-aligned FASTA files in:

```text
aligned/
```

---

### 🔹 Step 3: Generate SNP Data

Run the SNP script:

```bash
python3 SNP.py
```

👉 This reads the aligned files in `aligned/` and converts variable nucleotide positions into SNP data.

---

## 📌 Notes

- The `aligned/` folder is the main input for downstream SNP analysis.
- All sequences in the same input file should be homologous.
- Do not use unaligned sequences directly for SNP generation.
- For large datasets, it is recommended to complete the alignment first.
- `aligned.sh` requires MAFFT to function properly.
- The SNP output location and format are determined by the settings in `SNP.py`.

---

## 🧠 Pipeline Overview

| Processing step |
|:---:|
| **TestData** (FASTA sequences) |
| ↓ |
| **MAFFT** (`aligned.sh`) |
| ↓ |
| **aligned/** (alignment results) |
| ↓ |
| **SNP.py** |
| ↓ |
| **SNP data** |
