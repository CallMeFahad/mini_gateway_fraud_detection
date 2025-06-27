# mini gateway fraud detection
Analyzing bank data to identify anomalies and flag them as potentially fraudulent transactions &amp; xtracts the  merchant name &amp; total from the receipt image to feed a rules engine.

## Part A: Unsupervised Fraud Detection via K-Means Clustering
This report details the exploratory analysis, feature engineering, and clustering approach used to flag anomalous transactions in an unlabeled financial dataset.

### Dataset
We used a public financial transactions dataset with the following relevant fields:

- `TransactionID`: Unique ID for each transaction.
- `AccountID`: Unique ID for each account, linked to multiple transactions.
- `TransactionAmount`: Monetary value of the transaction.
- `TransactionDate`: Date and time of the transaction.
- `TransactionType`: Type of transaction, either 'Credit' or 'Debit.'
- `Location`: U.S. city where the transaction occurred.
- `DeviceID`: ID of the device used for the transaction.
- `IP_address`: IPv4 address associated with the transaction.
- `MerchantID`: Unique ID for the merchant involved in the transaction.
- `Channel`: Transaction channel (e.g., Online, ATM, Branch).

Since there were no labels provided, we considerd this as an **unsupervised anomaly detection problem**.
The dataset can be downloaded from [here](https://www.kaggle.com/datasets/valakhorasani/bank-transaction-dataset-for-fraud-detection/data)

### Exploratory Dataset Analysis:
- No null values were found.
- No duplicate values were found.
- Transactions were analyzed.
- Transactions amounts are heavily right-skewed, with debit transactions outnumbering credit transactions across all ranges.
- Most transactions took place on Monday.
- Most accounts have 4-5 unique devices and IP addresses, with both distributions following roughly normal patterns centered around typical user access behavior. Very few accounts show extreme variation (below 2 or above 8-9), suggesting consistent usage patterns across the user base.
- `TransactionAmount`, `CustomerAge`, `AccountBalance` were the features selected for model training. The features were scaled to be suitable for K-Means clustering.

### Model Training:
Once the values were scaled down, they were fitted in the K-Means model. Elbow plot analysis was performed, with the elbow forming at `n_clusters = 3`
Isolation Forest model was also implemented, which is an ensemble technique used for anomaly detection, suitable for our task.
