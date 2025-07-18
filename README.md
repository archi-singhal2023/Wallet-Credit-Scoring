# Credit Score Analysis Using Anomaly Detection

This project evaluates the creditworthiness of blockchain wallets based on their transaction behaviors using the **Isolation Forest** anomaly detection algorithm. The primary objective is to assign a score to each wallet that reflects its transaction behavior, enabling classification of wallets from low-risk to high-risk.

---

## 📂 Files Included

- `score_wallets.py` – Main script to process wallet transactions and generate scores.
- `user-wallet-transactions.json` – Input dataset containing transaction histories of wallets.
- `wallet_scores.csv` – Output file containing wallet IDs and their assigned scores.
- `score_distribution.png` – Visual representation of the distribution of wallet scores.
- `analysis.md` – Analytical insights based on the scores and their distributions.
- `README.md` – Project overview and documentation.

---

## 🧠 Methodology

### 🔍 Problem Statement

Given a set of wallets and their transaction history, the goal is to identify anomalous behaviors and assign a **score** that reflects transaction trustworthiness or risk.

### 🛠️ Steps Involved

1. **Data Parsing**: Load the transaction JSON file and extract per-wallet features.
2. **Feature Engineering**:
    - Number of transactions
    - Average transaction value
    - Transaction variance
    - Max transaction value
    - Unique addresses interacted with
3. **Isolation Forest Model**:
    - Used to detect outlier behavior (unsupervised).
    - Normalized anomaly scores to a 0–1000 scale for interpretability.
4. **Result Export**:
    - Scores saved to `wallet_scores.csv`
    - Score distribution visualized and saved as `score_distribution.png`

---

## 🤖 Model Choice: Isolation Forest

**Why Isolation Forest?**
- Suitable for unsupervised anomaly detection.
- Efficient on high-dimensional and large datasets.
- No assumptions about data distribution.

Other considered models are discussed in [`analysis.md`](./analysis.md).

---

## 📊 Score Interpretation

- **0–200**: Highly anomalous or suspicious wallets.
- **200–500**: Moderate anomaly; needs attention.
- **500–800**: Normal wallet behavior.
- **800–1000**: Highly trustworthy wallets.

---

## 🚀 How to Run

```bash
# Step 1: Install dependencies
pip install pandas scikit-learn matplotlib

# Step 2: Run the script
python score_wallets.py
