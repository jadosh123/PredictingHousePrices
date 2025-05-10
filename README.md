# PredictingHousePrices Getting Started

Follow these steps to set up the project and run the code:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/jadosh123/PredictingHousePrices.git
    cd PredictingHousePrices
    ```

2.  **Install dependencies:**
    ```bash
    ./setup_env.sh # On macOS/Linux
    bash setup_env.sh   # On Windows
    ```
    The `setup_env.sh` file lists the necessary Python libraries, such as pandas, numpy, scikit-learn, matplotlib, seaborn and tensorflow.

3.  **Download the dataset:**
    You need to manually download the dataset from kaggle and store it in
    `./kaggle_dataset` which should be located in the home directory of the project, if it does not exist you can create it, to download the dataset you need to set up your kaggle account with your api key and then run the command:
    `kaggle competitions download -c house-prices-advanced-regression-techniques`

## Running the Code

1.  **Data Exploration and Preprocessing:**
    * Open the jupyter-notebook called `data-cleaning.ipynb` to look at the step by step creation of this project and the visualization of the dataset.

2.  **Model Training and Evaluation:**
    * Open the file located at `./src/model.py` to train the model on te whole dataset and get a submission.csv file for predictions.


## Model Selection

The model selected was Tensorflow keras random forests regression model.

## Evaluation Metrics

The performance of the models will be evaluated using relevant regression metrics, such as:

* **Root Mean Squared Error (RMSE):** Square root of the MSE, providing an error in the same units as the target variable.
    $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$

## Further Improvements

Potential areas for future improvement include:

* Exploring more machine learning models.
* Performing more extensive feature engineering and selection.
* Fine-tuning hyperparameters using more sophisticated techniques.
* Addressing potential data leakage issues.

## Acknowledgements

The dataset used: `house-prices-advanced-regression-techniques`
