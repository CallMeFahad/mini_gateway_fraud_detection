import requests
import time

url = "http://127.0.0.1:8000/score"

txn = {
    "TransactionAmount": 8000.0,
    "CustomerAge": 19,
    "AccountBalance": 200.0
}

start = time.time()
res = requests.post(url, json=txn)
end = time.time()

print("Response:", res.json())
print(f"Latency: {(end - start) * 1000:.2f} ms")

import requests

# Test OCR
with open("receipt.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)
    print("OCR Result:", response.json())