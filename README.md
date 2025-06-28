# Mini gateway fraud detection
Analyzing bank data to identify anomalies and flag them as potentially fraudulent transactions &amp; xtracts the  merchant name &amp; total from the receipt image to feed a rules engine.

## Unsupervised Fraud Detection via K-Means Clustering
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

Since there were no labels provided, we considered this as an **unsupervised anomaly detection problem**.
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

### Optical Character Recognition:
OCR was implemented using the EasyOCR library for the English language. The reader reads the entire receipt and returns the text to the user, identifying merchant and the amounts.

## Installation

1. **Clone or download this project**
2. **Install required packages:**
   ```bash
   pip install fastapi uvicorn joblib numpy pandas pydantic scikit-learn easyocr opencv-python python-multipart
   ```

3. **Ensure your project folder contains:**
   ```
   your-project-folder/
   ├── app.py
   ├── scaler.pkl
   ├── kmeans_model.pkl (or isolation_forest_model.pkl)
   └── threshold.json
   ```

## Running the Application

### Method 1: Simple FastAPI (Recommended for testing)
```bash
uvicorn app:app --reload
```

### Method 2: Docker (Recommended for deployment)
```bash
# Build the image
docker build -t fraud-ocr-api .

# Run the container
docker run -p 8000:8000 fraud-ocr-api
```

## API Endpoints

Once running, your API will be available at `http://localhost:8000`

### 1. Fraud Detection - `/score`
**POST** request to detect potentially fraudulent transactions.

**Request Body:**
```json
{
  "TransactionAmount": 1000.0,
  "CustomerAge": 35.0,
  "AccountBalance": 5000.0
}
```

**Response:**
```json
{
  "KMeans_Cluster": 1,
  "Distance_to_Center": 0.234,
  "Potential_Fraud": false
}
```

### 2. Receipt OCR - `/ocr`
**POST** request to extract text from receipt images.

**Request:** Upload an image file (JPG, PNG, etc.)

**Response:**
```json
{
  "extracted_text": "WALMART STORE #1234 TOTAL: $45.67 THANK YOU"
}
```

## How to Test

### Option 1: Interactive Documentation (Easiest)
1. Start the application: `uvicorn fraud_detection_main:app --reload`
2. Open your browser and go to: `http://localhost:8000/docs`
3. You'll see an interactive interface where you can:
   - Test the fraud detection by entering transaction data
   - Upload receipt images for OCR processing

### Option 2: Using curl commands

**Test Fraud Detection:**
```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "TransactionAmount": 1500.0,
    "CustomerAge": 28.0,
    "AccountBalance": 3000.0
  }'
```

**Test OCR (replace 'receipt.jpg' with your image file):**
```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@receipt.jpg"
```

### Option 3: Using Python requests
```python
import requests

# Test fraud detection
fraud_data = {
    "TransactionAmount": 2000.0,
    "CustomerAge": 45.0,
    "AccountBalance": 8000.0
}

response = requests.post("http://localhost:8000/score", json=fraud_data)
print("Fraud Detection Result:", response.json())

# Test OCR
with open("receipt.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/ocr", files=files)
    print("OCR Result:", response.json())
```
(Also available in the ```api_testing.py``` file)
## Understanding the Results

### Fraud Detection Results
- **KMeans_Cluster**: Which cluster the transaction belongs to
- **Distance_to_Center**: How far the transaction is from the cluster center
- **Potential_Fraud**: `true` if distance exceeds threshold, `false` otherwise

### OCR Results
- **extracted_text**: All text found in the receipt image
- Look for merchant names (usually at the top) and total amounts (look for "TOTAL", "$", etc.)
