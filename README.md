# Backend Take-Home Exercise

## Introduction

Welcome to the backend take-home exercise! This repository contains a Flask-based service designed to process receipts and calculate loyalty points based on various conditions. The service handles receipt data, assigns points for qualifying purchases, and returns these points to the user.

## Application Overview

This backend application has the following features:
- **POST /receipts/process**: Accepts receipt details, processes them, and returns a unique receipt ID.
- **GET /receipts/<receiptId>/points**: Retrieves the calculated points for a given receipt ID.

### Key Features:
- Dynamic point calculation based on retailer name, total purchase amount, items bought, and more.
- Simple REST API built with Flask.
- Lightweight and easy to run in a Docker container.

## Prerequisites

To run the application, you'll need the following:
- **Docker**: The service is containerized and requires Docker to run. [Download Docker](https://www.docker.com/products/docker-desktop) if you don’t have it already installed.

### How to Set Up

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/JakubCzachor/receiptProcessor.git
   cd receiptProcessor
   ```
   
2. Build and run the Docker image
  ```bash
  docker build -t receiptProcessor .
  docker run -p 8000:8000 receiptProcessor
  ```

### API Endpoints

- POST /receipts/process
  - Submit a receipt to be processed. This endpoint calculates loyalty points and returns a unique receipt ID.
  - Parameters:
      - retailer: Name of the retailer (string).
      - total: Total purchase amount (float).
      - items: List of items purchased, with each item having:
      - shortDescription: Description of the item (string).
      - price: Price of the item (float).
      - purchaseDate: The date of the purchase in the format YYYY-MM-DD (string).
      - purchaseTime: The time of the purchase in HH:MM format (string).
   
- GET /receipts/<receiptId>/points
    - Get the calculated points for a specific receipt using its unique ID.


### Points Calculation Logic
  - Retailer Name Length: Points are awarded based on the number of alphanumeric characters in the retailer's name. Each alphanumeric character adds one point.
  - Total Purchase:
  - If the total ends with .00, 50 points are awarded.
  - If the total is a multiple of .25, 25 points are awarded.
  - Item Pairs: For every pair of items, 5 points are awarded.
  - Item Descriptions - If an item's description length is a multiple of 3, 20% of its price is added to the points.
  - Purchase Date: If the day of the month is odd, 6 points are added.
  - Purchase Time: If the purchase was made between 14:00 and 16:00, 10 points are added.


