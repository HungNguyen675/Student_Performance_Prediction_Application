import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def main():
    print("1. Loading Data...")
    df = pd.read_csv('student_data.csv')
    
    print("2. Data Preprocessing & Target Variable Creation...")
    # Convert grades from 20-point scale to 10-point scale
    df['G1'] = df['G1'] / 20 * 10
    df['G2'] = df['G2'] / 20 * 10
    df['G3'] = df['G3'] / 20 * 10
    
    # Create the completely new target variable: Average_Score
    df['Average_Score'] = (df['G1'] + df['G2'] + df['G3']) / 3
    
    # Feature Selection: Include G1, G2 and 10 study-related features
    selected_features = [
        'G1', 'G2', 'studytime', 'failures', 'absences', 'schoolsup', 'famsup', 
        'paid', 'higher', 'internet', 'freetime', 'goout'
    ]
    
    X = df[selected_features]
    y = df['Average_Score']
    
    print("3. Encoding Categorical Variables...")
    categorical_cols = X.select_dtypes(include=['object']).columns
    numeric_cols = X.select_dtypes(exclude=['object']).columns
    
    # Preprocessing pipelines for both numeric and categorical data
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])
    
    print("4. Train-Test Split...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("5. Training Regression Ensemble Model...")
    # Define Regressors
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
    svr = SVR(kernel='rbf')
    
    # Combine Regressors using VotingRegressor
    ensemble = VotingRegressor(estimators=[
        ('rf', rf),
        ('gb', gb),
        ('svr', svr)
    ])
    
    # Create a full pipeline with preprocessor and model
    model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                     ('model', ensemble)])
    
    # Train the pipeline
    model_pipeline.fit(X_train, y_train)
    
    print("6. Evaluating Model...")
    y_pred = model_pipeline.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nRoot Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R-squared Score (R2): {r2:.4f}")
    print("(R2 cang gan 1.0 thi mo hinh cang chinh xac)")
    
    print("\n7. Saving Model...")
    joblib.dump(model_pipeline, 'ensemble_model.pkl')
    joblib.dump(list(X.columns), 'feature_columns.pkl')
    print("Model saved successfully as ensemble_model.pkl!")

if __name__ == "__main__":
    main()
