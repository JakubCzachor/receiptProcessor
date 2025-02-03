from flask import Flask, request, jsonify
import uuid
import math

app = Flask(__name__)

#In-memory storage for receipts
receipts = {}

def calculateRetailerPoints(retailer):
    return sum(1 for c in retailer if c.isalnum())

def calculateTotalPoints(total):
    points = 0
    total = float(total)
    #Ends in X.00
    if total.is_integer():
        points += 50
    #Multiple of .25
    if total % 0.25 == 0:
        points += 25
    return points

def calculateItemsPoints(items):
    #5 points per pair of items
    points = 5 * (len(items) // 2)
    for item in items:
        if len(item['shortDescription'].strip()) % 3 == 0:
            #20% of price if description length is multiple of 3
            points += math.ceil(float(item['price']) * 0.2)
    return points

def calculateDatePoints(purchaseDate):
    return 6 if int(purchaseDate.split("-")[-1]) % 2 == 1 else 0

def calculateTimePoints(purchaseTime):
    return 10 if "14:00" <= purchaseTime <= "16:00" else 0

def calculatePoints(receipt):
    points = 0
    points += calculateRetailerPoints(receipt['retailer'])
    points += calculateTotalPoints(receipt['total'])
    points += calculateItemsPoints(receipt['items'])
    points += calculateDatePoints(receipt['purchaseDate'])
    points += calculateTimePoints(receipt['purchaseTime'])
    return points

@app.route("/receipts/process", methods=["POST"])
def processReceipt():
    """Process a receipt and return a unique ID."""
    receipt = request.json
    receiptId = str(uuid.uuid4())
    points = calculatePoints(receipt)
    receipts[receiptId] = points
    return jsonify({"id": receiptId})

@app.route("/receipts/<receiptId>/points", methods=["GET"])
def getPoints(receiptId):
    """Retrieve points for a given receipt ID."""
    if receiptId not in receipts:
        return jsonify({"error": "Receipt not found"}), 404
    return jsonify({"points": receipts[receiptId]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
