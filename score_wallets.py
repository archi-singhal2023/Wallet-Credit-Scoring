import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import argparse

def load_data(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

def extract_features(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['date'] = df['timestamp'].dt.date
        
    #Count of each action per wallet
    action_counts = df.pivot_table(index='userWallet', columns='action', aggfunc='size', fill_value=0)
    
    #Number of total transactions per wallet
    total_tx = df.groupby('userWallet').size().rename("total_transactions")
    
    #Active days
    active_days = df.groupby('userWallet')['date'].nunique().rename("active_days")
    
    #First and last activity to measure lifespan
    first_seen = df.groupby('userWallet')['timestamp'].min()
    last_seen = df.groupby('userWallet')['timestamp'].max()
    lifespan = (last_seen - first_seen).dt.days.rename("wallet_lifespan_days")
    
    #Combine all features
    features = pd.concat([action_counts, total_tx, active_days, lifespan], axis=1).fillna(0)
    features.columns = features.columns.astype(str)
    
    return features

# Applying unsupervised learning for scoring
def generate_scores(features):
    #Isolation Forest to detect outliers (risky users)
    model = IsolationForest(contamination = 0.05, random_state=42)
    model.fit(features)
    
    #Anomaly scores: lower is more risky
    anomaly_score = model.decision_function(features) # higher is better
    scaler = MinMaxScaler(feature_range=(300, 1000))
    
    credit_scores = scaler.fit_transform(anomaly_score.reshape(-1, 1)).flatten()
    features['credit_score'] = credit_scores.astype(int)
    
    return features.reset_index()

def save_scores(df, output_path='wallet_scores.csv'):
    df[['userWallet', 'credit_score']].to_csv(output_path, index=False)
    print(f"Saved credit scores to: {output_path}")

def score_range(scored_df):
    bins = list(range(0, 1100, 100))
    labels = [f"{i}-{i+99}" for i in bins[:-1]]
    
    scored_df['score_range'] = pd.cut(scored_df['credit_score'], bins=bins, labels=labels, right=False)
    score_distribution = scored_df['score_range'].value_counts().sort_index()
   
    # Plotting the score distribution
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    score_distribution.plot(kind='bar', color='skyblue')
    plt.title('Credit Score Distribution')
    plt.xlabel('Credit Score Range')
    plt.ylabel('Number of Wallets')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("score_distribution.png")  # fixed typo: distrivution → distribution
    plt.show()   

def main():
    print("Loading data...")
    df = load_data("user-wallet-transactions.json")
    
    print("Extracting features...")
    features = extract_features(df)
    
    print("Generating credit scores...")
    scored_df  = generate_scores(features)
    
    print("Saving final output...")
    save_scores(scored_df)
    
    print("Analyzing score distribution...")
    score_range(scored_df)

if __name__ == '__main__':
    main()

