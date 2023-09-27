# Flask-RESTful API  Insurance project

This project shows one of the possible ways to implement a RESTful API server for insurance applications.

There are implemented two models: user_data and cart_data, one user can have many insurances.

Main libraries used:
1. Flask-PyMongo - for handling all MongoDB database operations.
2. Flask-RESTful - restful API library.
3. Flask-Script - provides support for writing external scripts.
4. bson - BSON (Binary JSON) encoding and decoding.

Project structure:
```
.
├── README.md
├── app.py
├── samplerates.csv
├── helper.py
└── requirements.txt
```

* app.py - holds all endpoints.
* app.py - flask application initialization.
* samplerates.csv - all CSV data for parsing.
* helper.py - for supporting functions and helper functions for API actions

## Running 

1. Clone repository.
2. pip install requirements.txt
3. Run the flask app.py
4. Use Postman for accessing the API endpoints

## Usage
### Users endpoint
POST http://127.0.0.1:5000/user_input

REQUEST
```json
{
  "user_data": [
    {
      "name": "Naga Ajay",
      "age_range": "23",
      "tier": "tier-1",
      "member_csv": "1a",
      "sum_assured": 500000
    }
  ]
}
```
RESPONSE
```json
{
    "message": "User input stored successfully",
    "user_id": "6513db5ee4c64d685faa6115"
}
```
POST http://127.0.0.1:5000/calculate_premium

REQUEST
```json
{
    "_id": "6513db5ee4c64d685faa6115"
}
```
RESPONSE
```json
{
    "premium": [
        {
            "age_range": "23",
            "member_csv": "1a",
            "name": "Naga Ajay",
            "premium": "4567.0",
            "sum_assured": 500000,
            "tier": "tier-1"
        }
    ]
}
```
POST http://127.0.0.1:5000/add_to_cart

REQUEST
```json
{
  "primaryID": "6513db5ee4c64d685faa6115",
  "user_premium_data": [
        {
            "age_range": "23",
            "member_csv": "1a",
            "name": "Naga Ajay",
            "premium": "4567.0",
            "sum_assured": 500000,
            "tier": "tier-1"
        }
    ]
}
```
RESPONSE
```json
{
    "cart_data": [
        {
            "age_range": "23",
            "member_csv": "1a",
            "name": "Naga Ajay",
            "premium": "4567.0",
            "sum_assured": 500000,
            "tier": "tier-1"
        }
    ],
    "cart_data_id": "6513dc6ee4c64d685faa6116",
    "message": "Insurance plan added to cart"
}
```
POST http://127.0.0.1:5000/verify_purchase

REQUEST
```json
{
    "cart_data": [
        {
            "age_range": "23",
            "member_csv": "1a",
            "name": "Naga Ajay",
            "premium": "4567.0",
            "sum_assured": 500000,
            "tier": "tier-1"
        }
    ],
    "cart_data_id": "6513dc6ee4c64d685faa6116"
}
```
RESPONSE
```json
{
    "message": "Purchase verified"
}
```
GET http://127.0.0.1:5000/get_all_cart_data
```json
{
    "Carts": [
        {
            "primaryID": "6513db5ee4c64d685faa6115",
            "user_premium_data": [
                              {
                                  "age_range": "23",
                                  "member_csv": "1a",
                                  "name": "Naga Ajay",
                                  "premium": "4567.0",
                                  "sum_assured": 500000,
                                  "tier": "tier-1"
                              }
                            ]
        }
    ]
}
```
GET http://127.0.0.1:5000/get_all_user_data
```json
{
    "Users": [
    {
      "name": "Naga Ajay",
      "age_range": "23",
      "tier": "tier-1",
      "member_csv": "1a",
      "sum_assured": 500000
    }
  ]
}
```
All are JSON data, please same field names only.
