import pandas as pd


# Drops majority null features
def drop_null_majority_features(df_train: pd.DataFrame, df_test: pd.DataFrame):
    cols_to_drop = []
    for col in df_train.columns:
        if df_train[col].isnull().sum() > len(df_train[col])/2:
            cols_to_drop.append(col)

    df_train.drop(cols_to_drop, axis=1, inplace=True)
    df_test.drop(cols_to_drop, axis=1, inplace=True)
