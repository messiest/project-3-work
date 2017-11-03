import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib


if __name__ == "__main__":
    print("kNN Classifier")
    knn = KNeighborsClassifier(n_jobs=-1)

    df_chunk = pd.read_csv('../processed_data/train_data.csv', chunksize=10000)
    print("Data loaded")
    print("Fitting model...")
    df_train = pd.concat(df_chunk, ignore_index=True)

    y_train = df_train.pop('response_df')
    x_train = df_train

    _ = knn.fit(x_train, y_train)
    _ = joblib.dump(knn, '../jar/knn.pkl')
    print("Fitting Complete\nTrained model can be found at ../jar/knn.pkl")

