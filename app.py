from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo.mongo_client import MongoClient
from helper import *
from bson.objectid import ObjectId
from bson import json_util
import json

app = Flask(__name__)
cors = CORS(app,resources=r'/api/*')
# app.config['CORS_HEADERS'] = 'Content-Type'
# MongoDB database uri
uri = "mongodb+srv://nagaajayk:HxeFYNVbrRCzv@clusterinsurance.c6dlms6.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# @app.route('/')
# def index():
#     return "Connected to the data base!"

# @app.route("/add_one")
# def add_one():
#     try:
#         client.db.Users.insert_one({'title': "todo Ajay", 'body': "todo body"})
#         return jsonify(message="success")
#     except Exception as e:
#         return jsonify({'message': 'User is not stored', 'Error': e})



@app.route('/api/v1/user_input', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
def user_input():
    print("user_input",request.json)
    data = request.json  
    # Assuming JSON data with age, sum_insured, city_tier, and tenure
    # Store user input in MongoDB
    # print(data)
    try: 
      print(data)
      user_collection = client.db.Users
      user_id = user_collection.insert_one(data).inserted_id
      return jsonify({"message" : "User input stored successfully","user_id":str(user_id)})
    except Exception as e:
        print(e)
        return jsonify({'message': 'User is not stored', 'Error': e})
     
@app.route('/api/v1/calculate_premium', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
def calculate_premium():
    # data1=json_util.dumps(request)
    # print("data1",data1)
    print(request)
    data = request.json
    try:
        print("calculate_premium data",data)
        objInstance = ObjectId(data["_id"])
        user_object=client.db.Users.find_one(objInstance)
        print("user_data: ",user_object)
        print("number of users",len(user_object['user_data']))
        people_type={"1a":0,"1c":0}
        # for i in range(len(user_object['user_data'])):
        #     if user_object['user_data'][i]["member_csv"]=="1a":
        #         people_type['1a']+=1
        #     elif user_object['user_data'][i]["member_csv"]=="1c":
        #         people_type['1c']+=1
        for item in user_object['user_data']:
            if item["member_csv"]=="1a":
                people_type['1a']+=1
            elif item["member_csv"]=="1c":
                people_type['1c']+=1
        print("people_type",people_type)
        if people_type["1a"] ==0 or people_type["1a"] >2 or people_type["1c"] >4:
            return jsonify({'premium': []})
        else:
            if people_type["1c"]>0:
                string_type=str(people_type["1a"])+"a"+","+str(people_type["1c"])+"c"
            else:
                string_type=str(people_type["1a"])+"a"
        print("string_type",string_type)
        premium_list=[]
        for item in user_object['user_data']:
            print("single user item from list",item)
            premium_data = calculate_premium_logic(item,string_type)
            print("premium_one",premium_data[str(item['sum_assured'])])
            item['premium']=premium_data[str(item['sum_assured'])]
            premium_list.append(item)
        print("premium_list",premium_list)
        filter = { '_id': data['_id'] }
        newvalues = { "$set": {'user_data':premium_list }}
        client.db.Users.update_one(filter,newvalues,upsert=True)
        return jsonify({'premium': premium_list})
        
        # return json.loads(json_util.dumps(user_object))    
    except Exception as e:
        print("error from calculate premium",e)
        return jsonify({'message': 'Error in computing the premium', 'Error': e})
    

@app.route('/api/v1/add_to_cart', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
def add_to_cart():
    try:
        data = request.json
        print("add_to_cart: ",data['user_premium_data'])
        sorted_data = sorted(data["user_premium_data"], key=lambda x: int(x["age_range"]))  
        print("cart_premium_list: ",sorted_data)
        data["Total"]=0.0
        if len(sorted_data)>1:
            for i in range(len(sorted_data)-1):
                sorted_data[i]['floater_discount']="50"
                sorted_data[i]['discounted_rate']=float(sorted_data[i]['premium'])*0.5
                data["Total"]+=float(sorted_data[i]['discounted_rate'])
            sorted_data[len(sorted_data)-1]['floater_discount']="00"
            sorted_data[len(sorted_data)-1]['discounted_rate']=sorted_data[len(sorted_data)-1]['premium']
            data["Total"]+=float(sorted_data[len(sorted_data)-1]['discounted_rate'])
        else:
            sorted_data[len(sorted_data)-1]['floater_discount']="00"
            sorted_data[len(sorted_data)-1]['discounted_rate']=sorted_data[len(sorted_data)-1]['premium']
            data["Total"]+=float(sorted_data[len(sorted_data)-1]['discounted_rate'])
        data['user_premium_data']=sorted_data
        cart_data=client.db.cart.insert_one(data).inserted_id
        return jsonify({'message': 'Insurance plan added to cart','cart_data_id':str(cart_data),'cart_data':data['user_premium_data'],'Total':data['Total']})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error in adding to the cart', 'Error': e})



@app.route('/api/v1/verify_purchase', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
def verify_purchase():
    try:
        data = request.json
        print("verify-pruchase data: ",data)
        filter = { '_id': data['cart_data_id'] }
        newvalues = { "$set": {'user_premium_data':data['cart_data'],'premium_sold':True }}
        client.db.cart.update_one(filter,newvalues,upsert=True)
        return jsonify({'message': 'Purchase verified'})

    except Exception as e:
        print(e)
        return jsonify({'message': 'Error in verifying the purchase', 'Error': e})
    

@app.route('/api/v1/get_all_user_data', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_all_user_data():
    try:
        users = list(client.db.Users.find({}))
        print(users)
        return jsonify({"Users":str(users)})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error in getting the users data', 'Error': e})


@app.route('/api/v1/get_all_cart_data', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_all_cart_data():
    try:
        carts = list(client.db.cart.find({}))
        print(carts)
        return jsonify({"Carts":str(carts)})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error in getting the cart data', 'Error': e})


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
