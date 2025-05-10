import pandas as pd
import tensorflow_decision_forests as tfdf
import data_utils as du
from sklearn.preprocessing import StandardScaler

# Load datasets
df_train = pd.read_csv("kaggle_dataset/train.csv")
df_test = pd.read_csv("kaggle_dataset/test.csv")

# Drop Id column
df_train = df_train.drop('Id', axis=1)

# Dispose of majority null columns
du.drop_null_majority_features(df_train, df_test)

# Dispose of single value majority features
du.drop_single_val_majority(df_train, df_test)

# Standardize the data
df_num = df_train.select_dtypes(include=['int64', 'float64'])
df_num.drop('SalePrice', axis=1, inplace=True)

df_num_cols = df_num.columns
scaler = StandardScaler()
scaler.fit(df_train[df_num_cols])
df_train[df_num_cols] = scaler.transform(df_train[df_num_cols])
df_test[df_num_cols] = scaler.transform(df_test[df_num_cols])

# Feature Engineering
df_train['TotalSF'] = (
    df_train['GrLivArea'] + df_train['1stFlrSF'] + df_train['TotalBsmtSF']
)
df_test['TotalSF'] = (
    df_test['GrLivArea'] + df_test['1stFlrSF'] + df_test['TotalBsmtSF']
)

df_train['GarageSize'] = df_train['GarageCars'] + df_train['GarageArea']
df_test['GarageSize'] = df_test['GarageCars'] + df_test['GarageArea']

df_train['TotalRoomSfAboveGr'] = (
    df_train['1stFlrSF'] + df_train['2ndFlrSF'] + df_train['GarageCars']
)
df_test['TotalRoomSfAboveGr'] = (
    df_test['1stFlrSF'] + df_test['2ndFlrSF'] + df_test['GarageCars']
)

df_train['HouseValue'] = (
    df_train['OverallQual'] + df_train['OverallCond'] +
    df_train['TotalRoomSfAboveGr']
)
df_test['HouseValue'] = (
    df_test['OverallQual'] + df_test['OverallCond'] +
    df_test['TotalRoomSfAboveGr']
)

df_train['BdRmPerRoom'] = (
    df_train['BedroomAbvGr'] / df_train['TotRmsAbvGrd']
)
df_test['BdRmPerRoom'] = (
    df_test['BedroomAbvGr'] / df_test['TotRmsAbvGrd']
)

df_train['TotalBathrooms'] = (
    df_train['BsmtFullBath'] + df_train['FullBath'] + df_train['HalfBath']
)
df_test['TotalBathrooms'] = (
    df_test['BsmtFullBath'] + df_test['FullBath'] + df_test['HalfBath']
)

df_train['TotalRooms'] = (
    df_train['TotalBathrooms'] + df_train['TotRmsAbvGrd']
)
df_test['TotalRooms'] = (
    df_test['TotalBathrooms'] + df_test['TotRmsAbvGrd']
)

df_train['HouseQual'] = df_train['OverallCond'] + df_train['OverallQual']
df_test['HouseQual'] = df_test['OverallCond'] + df_test['OverallQual']

df_train['lastRenov'] = (
    (df_train['YearRemodAdd'] - df_train['YearBuilt']) ** 2
) / 2
df_test['lastRenov'] = (
    (df_test['YearBuilt'] - df_test['YearRemodAdd']) ** 2
) / 2

df_train['renovCondCombined'] = (
    (df_train['lastRenov'] / df_train['lastRenov'].max()) *
    df_train['OverallCond']
)
df_test['renovCondCombined'] = (
    (df_test['lastRenov'] / df_test['lastRenov'].max()) *
    df_test['OverallCond']
)

# Convert to tensorflow dataset
label = 'SalePrice'
train_ds = tfdf.keras.pd_dataframe_to_tf_dataset(
    df_train,
    label=label,
    task=tfdf.keras.Task.REGRESSION
)

# Configure and Train model
# Configure the model
rf = tfdf.keras.RandomForestModel(
    hyperparameter_template="benchmark_rank1",
    task=tfdf.keras.Task.REGRESSION,
    num_trees=600,
    min_examples=4,
    bootstrap_size_ratio=3.0,
    bootstrap_training_dataset=True
    )
rf.compile(metrics=['mse'])
rf.fit(x=train_ds)
save_path = "../temp/my_rf_model"
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
