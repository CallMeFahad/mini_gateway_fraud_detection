from fastapi import FastAPI, File, UploadFile, HTTPException
import joblib
import numpy as np
from pydantic import BaseModel
import pandas as pd
import json
import tempfile
import cv2
import os
import easyocr

#Loading the scaler and the model
scaler = joblib.load('scaler.pkl')
model = joblib.load('kmeans_model.pkl') #Write 'isolation_forest_model.pkl' if using Isolation Forest

#Initializing the FastAPI app
app = FastAPI(title="Mini Gateway Fraud Detection")

#Initializing the OCR reader
reader = easyocr.Reader(['en'], gpu=False)  # Changed to False to avoid GPU issues

#Defining the expected input fields for transaction
class TransactionInput(BaseModel):
    TransactionAmount: float
    CustomerAge: float
    AccountBalance: float

@app.post("/score")
def score_transaction(transaction: TransactionInput):
    input_data = pd.DataFrame([transaction.model_dump()])  # Renamed 'input' to avoid conflict

    #Scaling the input
    scaled_input = scaler.transform(input_data)
    
    #Setting the threshold
    with open("threshold.json") as f:
        threshold = json.load(f)["threshold"]

    #Predicting the cluster
    prediction = model.predict(scaled_input)

    #finding the centroid it belongs to
    centroid = model.cluster_centers_[prediction]

    #Calculating the distance from the centroid
    distance = np.linalg.norm(scaled_input[0] - centroid)

    anomaly = distance > threshold

    return {
        "KMeans_Cluster": int(prediction[0]),  # Fixed indexing
        "Distance_to_Center": float(distance),
        "Potential_Fraud": bool(anomaly)
    }

@app.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    """Extract text from receipt images"""
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read the uploaded file
        contents = await file.read()
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(contents)
            tmp_file_path = tmp_file.name
        
        try:
            # Load the image using OpenCV
            img = cv2.imread(tmp_file_path)
            
            if img is None:
                raise HTTPException(status_code=400, detail="Could not process the image")
            
            # Convert to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Perform OCR
            results = reader.readtext(gray_img)
            
            # Extract text
            extracted_texts = []
            
            for res in results:
                bbox, detected_text, confidence = res
                if confidence > 0.2 and len(detected_text.strip()) > 1:
                    extracted_texts.append(detected_text.strip())
            
            # Join all extracted text
            full_text = " ".join(extracted_texts)
            
            return {
                "extracted_text": full_text
            }
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during OCR processing: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)