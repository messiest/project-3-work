import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib


if __name__ == "__main__":
    print("Decision Tree - Content")
    knn = DecisionTreeClassifier()

    df_chunks = pd.read_csv('../processed_data/train_data.csv', chunksize=10000)
    print("Data loaded")
    print("Fitting model...")
    df_train = pd.concat(df_chunks, ignore_index=True)


    y_train = df_train.pop('response_df')
    x_train = df_train[['has_emoji_df', 'outside_content_df', 'is_question_df', 'minutes_since_post_df']]

    _ = knn.fit(x_train, y_train)
    _ = joblib.dump(knn, '../jar/content_tree.pkl')
    print("Fitting complete\nTrained model can be found at ../jar/content_tree.pkl")

