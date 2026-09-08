import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_distribution():
    if not os.path.exists('data/annotations.csv'):
        print("annotations.csv not found. Please run data_prep.py first.")
        return
        
    df = pd.read_csv('data/annotations.csv')
    train_df = df[df['split'] == 'train']
    
    attributes = ['location', 'healing_status', 'closure_method', 'exudate_type', 
                  'erythema', 'edema', 'infection_risk', 'urgency_level']
                  
    print("=======================================")
    print(f"TRAIN SPLIT DISTRIBUTION (Total: {len(train_df)})")
    print("=======================================")
    
    os.makedirs('plots', exist_ok=True)
    
    for attr in attributes:
        counts = train_df[attr].value_counts()
        print(f"\n--- {attr.upper()} ---")
        for cls_name, count in counts.items():
            print(f"{cls_name}: {count} ({count/len(train_df)*100:.1f}%)")
            
        plt.figure(figsize=(10, 6))
        sns.barplot(x=counts.index, y=counts.values)
        plt.title(f'Train Distribution: {attr}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'plots/dist_{attr}.png')
        plt.close()
        
    print("\nCheck the 'plots/' directory for visualizations.")

if __name__ == "__main__":
    analyze_distribution()
