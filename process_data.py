import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

sampling = True

if __name__ == "__main__":
    print("Processing Data...\n")

    chunks = pd.read_csv('cleaned_data/processed_data.csv', chunksize=10000)
    df = pd.concat(chunks, ignore_index=True)
    print("Data Imported")

    df = df.drop_duplicates('post_id', keep='last')

    df = df.drop(['karma', 'comment_karma'], axis=1)
    comment_threshold = df.groupby('subreddit').quantile(.9).reset_index()[['subreddit', 'comments']].set_index('subreddit').transpose()

    # Build Response Vector
    response = []
    for i, row in df.iterrows():
        subreddit = row['subreddit']
        comments = row['comments']
        is_greater = 0
        if comments > comment_threshold[subreddit].values:
            is_greater = 1
        response.append(is_greater)
    df['response'] = response
    df = df.dropna()

    df_true = df[df['response'] == 1]
    df_false = df[df['response'] == 0]

    sample_size = int(0.5 * len(df_true))

    print(sample_size)
    if sampling:
        df_1 = df_true.sample(n=sample_size)
        df_0 = df_false.sample(n=sample_size)

    df = pd.concat([df_1, df_0])

    print(df.shape)

    print("Output Size: {}".format(df.shape[0]))

    subreddit_dummies = pd.get_dummies(df['subreddit'])
    print("Built subreddit dummies")

    sia = SIA()
    sentiment = df['title'].apply(sia.polarity_scores)
    sent = pd.DataFrame(list(sentiment))
    df = df.join(sent)
    print("Completed sentiment analysis")

    to_drop = ['comments', 'author', 'content', 'link', 'post_id',
               'subreddit', 'scrape_time', 'post_time', 'elapsed_time']

    df = df.drop(to_drop, axis=1)

    print("Dropped erroneous features")

    df = df.join(subreddit_dummies)  # join dummies

    df_train, df_test = train_test_split(df, test_size=0.3)  # 70/30 train/test split
    del df

    print('Training Data: n={}'.format(df_train.shape[0]))
    tfidf_percent = 0.05
    tfidf = TfidfVectorizer(stop_words='english',
                            strip_accents='unicode',
                            max_features=int(df_train.shape[0] * tfidf_percent))
    tfidf.fit(df_train)
    print("TFIDF Fit")

    tfidf_train = pd.DataFrame(tfidf.transform(df_train['title']).todense(), columns=tfidf.get_feature_names())
    df_train = df_train.drop('title', axis=1)
    df_train = df_train.join(tfidf_train, lsuffix='_df')
    df_train.fillna(0.0, inplace=True)
    df_train.to_csv('processed_data/train_data.csv', index=False, chunksize=1000)  # write training data
    del df_train

    print('Testing Data: n={}'.format(df_test.shape[0]))
    tfidf_test = pd.DataFrame(tfidf.transform(df_test['title']).todense(), columns=tfidf.get_feature_names())
    df_test = df_test.drop('title', axis=1)
    df_test = df_test.join(tfidf_test, lsuffix='_df')
    df_test.fillna(0.0, inplace=True)
    df_test.to_csv('processed_data/test_data.csv', index=False, chunksize=1000)  # write testing data
    del df_test

    print("Completed")
