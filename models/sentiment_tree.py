import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib


if __name__ == "__main__":
    print("Decision Tree - Sentiment")
    knn = DecisionTreeClassifier()

    df_chunks = pd.read_csv('../processed_data/train_data.csv', chunksize=10000)
    print("Data loaded")
    print("Fitting model...")

    df_train = pd.concat(df_chunks, ignore_index=True)

    y_train = df_train.pop('response_df')
    x_train = df_train[['neg_df', 'pos_df']]

    _ = knn.fit(x_train, y_train)
    _ = joblib.dump(knn, '../jar/sentiment_tree.pkl')
    print("Fitting Complete\nTrained model can be found at ../jar/sentiment_tree.pkl")

