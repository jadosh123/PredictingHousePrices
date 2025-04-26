import pandas as pd
import tensorflow_decision_forests as tfdf
import data_utils as du


# Load datasets
df_train = pd.read_csv("kaggle_dataset/train.csv")
df_test = pd.read_csv("kaggle_dataset/test.csv")

# Drop Id column
df_train = df_train.drop('Id', axis=1)

# Dispose of majority null columns
du.drop_null_majority_features(df_train, df_test)

# Dispose of single value majority features
du.drop_single_val_majority(df_train, df_test)

# Feature Engineering
df_train['TotalSF'] = df_train['GrLivArea'] + df_train['1stFlrSF']
+ df_train['TotalBsmtSF']
df_test['TotalSF'] = df_test['GrLivArea'] + df_test['1stFlrSF']
+ df_test['TotalBsmtSF']

df_train['BdRmPerRoom'] = df_train['BedroomAbvGr'] / df_train['TotRmsAbvGrd']
df_test['BdRmPerRoom'] = df_test['BedroomAbvGr'] / df_test['TotRmsAbvGrd']

df_train['TotalBathrooms'] = df_train['BsmtFullBath'] + df_train['FullBath']
+ df_train['HalfBath']
df_test['TotalBathrooms'] = df_test['BsmtFullBath'] + df_test['FullBath']
+ df_test['HalfBath']

df_train['TotalRooms'] = df_train['TotalBathrooms'] + df_train['TotRmsAbvGrd']
df_test['TotalRooms'] = df_test['TotalBathrooms'] + df_test['TotRmsAbvGrd']

# Convert to tensorflow dataset
label = 'SalePrice'
train_ds = tfdf.keras.pd_dataframe_to_tf_dataset(
    df_train,
    label=label,
    task=tfdf.keras.Task.REGRESSION
)

# Configure and Train model
rf = tfdf.keras.RandomForestModel(
    hyperparameter_template="benchmark_rank1",
    task=tfdf.keras.Task.REGRESSION,
    num_trees=400,
    max_depth=15,
    min_examples=1
    )
rf.compile(metrics=['mse'])
rf.fit(x=train_ds)
save_path = "../tmp/my_rf_model"
rf.save(save_path)

# Generate predictions and save to submission.csv
ids = df_test.pop('Id')
test_ds = tfdf.keras.pd_dataframe_to_tf_dataset(
    df_test,
    task=tfdf.keras.Task.REGRESSION
)
preds = rf.predict(test_ds)
output = pd.DataFrame({'Id': ids, 'SalePrice': preds.squeeze()})

output.to_csv('submission.csv', index=False)
