import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, accuracy_score
from imblearn.over_sampling import SMOTE
import pickle
import os
import glob

def handle_outliers(df, column):
    if column not in df.columns:
        return df
    # Simple log transformation for outliers in premium/amount
    df[column] = np.log1p(df[column])
    return df

def train_domain(csv_path, domain_name):
    print(f"\n--- Training Domain: {domain_name.upper()} ---")
    # Load data
    df = pd.read_csv(csv_path)
    
    # Milestone 2: Handling Outliers
    df = handle_outliers(df, 'policy_annual_premium')
    df = handle_outliers(df, 'total_claim_amount')
    
    # Feature Engineering
    cols_to_drop = ['claim_id', 'injury_claim', 'property_claim', 'vehicle_claim']
    cols_present_to_drop = [c for c in cols_to_drop if c in df.columns]
    df = df.drop(columns=cols_present_to_drop)
    
    # Handle categorical variables
    categorical_cols = df.select_dtypes(include=['object']).columns
    le_dict = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le
    
    # Split data
    X = df.drop('fraud', axis=1)
    y = df['fraud']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Milestone 2: Handling Imbalanced Dataset (SMOTE)
    try:
        smote = SMOTE(random_state=42)
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    except Exception as e:
        print(f"SMOTE failed for {domain_name} (likely too few samples): {e}")
        X_train_res, y_train_res = X_train, y_train
    
    # Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_res)
    X_test_scaled = scaler.transform(X_test)
    
    # Models to compare
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGboost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    }
    
    # Fallback to first model if no best found
    best_f1 = -1
    best_model = list(models.values())[0]
    best_name = list(models.keys())[0]
    
    for name, model in models.items():
        model.fit(X_train_scaled, y_train_res)
        y_pred = model.predict(X_test_scaled)
        f1 = f1_score(y_test, y_pred)
        
        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            best_name = name
            
    print(f"Best Model for {domain_name}: {best_name} (F1: {best_f1:.4f})")
    
    # Save artifacts
    save_dir = f'v:/blog-social login/claimwatch-ai/models/{domain_name}'
    os.makedirs(save_dir, exist_ok=True)
    
    with open(f'{save_dir}/model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    with open(f'{save_dir}/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    with open(f'{save_dir}/label_encoders.pkl', 'wb') as f:
        pickle.dump(le_dict, f)
    with open(f'{save_dir}/feature_names.pkl', 'wb') as f:
        pickle.dump(X.columns.tolist(), f)
    
    # Also save to default root if it's automobile for backward compatibility
    if domain_name == 'automobile':
        root_model_dir = 'v:/blog-social login/claimwatch-ai/models'
        for file in ['model.pkl', 'scaler.pkl', 'label_encoders.pkl', 'feature_names.pkl']:
            import shutil
            shutil.copy(f'{save_dir}/{file}', f'{root_model_dir}/{file}')

def train_all():
    data_dir = 'v:/blog-social login/claimwatch-ai/data'
    csv_files = glob.glob(f"{data_dir}/*_claims.csv")
    
    for csv_file in csv_files:
        domain_name = os.path.basename(csv_file).replace('_claims.csv', '')
        train_domain(csv_file, domain_name)

if __name__ == "__main__":
    train_all()
