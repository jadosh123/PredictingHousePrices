import pandas as pd
import tensorflow_decision_forests as tfdf


# Load datasets
df_train = pd.read_csv("kaggle_dataset/train.csv")
df_test = pd.read_csv("kaggle_dataset/test.csv")

df_train = df_train.drop('Id', axis=1)

cols_to_drop = []
for col in df_train.columns:
    if df_train[col].isnull().sum() > len(df_train[col])/2:
        cols_to_drop.append(col)

df_train.drop(cols_to_drop, axis=1, inplace=True)
df_test.drop(cols_to_drop, axis=1, inplace=True)

label = 'SalePrice'
train_ds = tfdf.keras.pd_dataframe_to_tf_dataset(
    df_train,
    label=label,
    task=tfdf.keras.Task.REGRESSION
)

rf = tfdf.keras.RandomForestModel(hyperparameter_template="benchmark_rank1",
                                  task=tfdf.keras.Task.REGRESSION)
rf.compile(metrics=['mse'])
rf.fit(x=train_ds)
save_path = "/tmp/my_rf_model"
rf.save(save_path)

ids = df_test.pop('Id')

test_ds = tfdf.keras.pd_dataframe_to_tf_dataset(
    df_test,
    task=tfdf.keras.Task.REGRESSION
)

preds = rf.predict(test_ds)
output = pd.DataFrame({'Id': ids, 'SalePrice': preds.squeeze()})

output.to_csv('submission.csv', index=False)
