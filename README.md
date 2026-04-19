# 📘 README

## 📂 專案說明
本專案用於處理基因序列資料，流程包含：
1. 原始序列整理  
2. 序列比對（Alignment）  
3. SNP 資料生成  

---

## 📁 資料結構

project/
│
├── TestData/        # 原始序列資料
├── aligned/         # 已完成比對的序列（可直接使用）
├── aligned.sh       # 批次比對腳本（使用 MAFFT）
├── SNP.py           # SNP 生成程式
└── README.md

---

## ⚙️ 環境需求

請先安裝 MAFFT

### 安裝方式（範例）

Linux / WSL：
sudo apt-get install mafft

Mac：
brew install mafft

---

## 🚀 使用流程

### 🔹 Step 1：準備資料
將原始序列檔案放入：

TestData/

---

### 🔹 Step 2：序列比對（Alignment）

有兩種方式：

方法一：使用腳本（推薦）

bash aligned.sh

👉 會自動將 TestData/ 內的檔案做 MAFFT 比對  
👉 輸出結果會放到 aligned/

方法二：直接使用已比對資料

aligned/

---

### 🔹 Step 3：產生 SNP 資料

python SNP.py

👉 會將 aligned/ 裡的資料轉換為 SNP 格式  

---

## 📌 補充說明

- aligned/ 資料夾為後續分析的主要輸入來源  
- 若資料量大，建議先完成 alignment 再進行 SNP 分析  
- aligned.sh 需搭配 MAFFT 使用，未安裝將無法執行  

---

## 🧠 流程概念（簡單版）

TestData (原始資料)
        ↓
MAFFT (aligned.sh)
        ↓
aligned (比對結果)
        ↓
SNP.py
        ↓
SNP 資料
