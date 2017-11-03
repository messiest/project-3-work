import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib


if __name__ == "__main__":
    forest = RandomForestClassifier(n_jobs=-1)
    print("Random Forest Classifier") 
    df_chunks = pd.read_csv('../processed_data/train_data.csv', chunksize=10000)
    print("Loading Data...")
    df_train = pd.concat(df_chunks, ignore_index=True)
    print("Done")
    y_train = df_train.pop('response_df')
    x_train = df_train
    print("Fitting model...")
    forest.fit(x_train, y_train)
    joblib.dump(forest, '../jar/forest.pkl')
    print("Fitting Complete\nTrained Model can be found at ../jar/forest.pkl")
