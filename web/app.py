
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017/')
db = client.Bank_Transactions
users = db['users']

def get_status_response(code):
    messages = {
        301: "Invalid Username.",
        302: "Incorrect Password.",
        303: "Not Enough Money!",
        304: "Invalid Amount (Must be ≥ 0)",
        305: "User already registered",
        306: "Required data is missing. Please ensure all necessary fields are provided.",
        307: "Transaction Failed. Couldn't find the target user",
        308: "You have no Loan right now. Loan payment cancelled."
    }

    message = messages.get(code, "Unknown Error")
    return {
        "Status code": code,
        "Message": message
    }
def check_existence(username):
    return bool(users.find_one({"Username": username}))
def verify_password(username, password):
    stored_hash = users.find_one({"Username": username})["Password"]
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

class Register(Resource):
    def post(self):
        get_posted_data = request.get_json()
        username = get_posted_data.get("username")
        password = get_posted_data.get("password")
        if not username or not password:
            return jsonify(get_status_response(306))
        if check_existence(username):
            return jsonify(get_status_response(305))
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.insert_one({"Username": username, "Password": hashed_pw,
                          "Balance": 0,
                          "Loan": 0})
        return jsonify({
            "Status code": 200,
            "Message": "User Registered Successfully"
        })

class Add(Resource):
    def post(self):
        get_posted_data = request.get_json()
        username = get_posted_data.get("username")
        password = get_posted_data.get("password")
        add_amount = get_posted_data.get("add_amount")
        if not username or not password or not add_amount:
            return jsonify(get_status_response(306))
        if not check_existence(username):
            return jsonify(get_status_response(301))
        if not verify_password(username, password):
            return jsonify(get_status_response(302))
        if int(add_amount) <= 0:
            return jsonify(get_status_response(304))
        old_balance = users.find_one({"Username": username})["Balance"]
        new_balance = int(add_amount) + int(old_balance)
        users.update_one({"Username": username}, {"$set": {"Balance": new_balance,}})
        return jsonify({
            "Status code": 200,
            "Message": "Success! Money Added"
        })

class Transfer(Resource):
    def post(self):
        get_posted_data = request.get_json()
        username = get_posted_data.get("username")
        password = get_posted_data.get("password")
        target_user = get_posted_data.get("target_user")
        transfer_amount = get_posted_data.get("transfer_amount")
        if not username or not password or not transfer_amount or not target_user:
            return jsonify(get_status_response(306))
        if not check_existence(username):
            return jsonify(get_status_response(301))
        if not verify_password(username, password):
            return jsonify(get_status_response(302))
        if users.find_one({"Username": username}).get("Balance") < transfer_amount:
            return jsonify(get_status_response(303))
        if not check_existence(target_user):
            return jsonify(get_status_response(307))
        if int(transfer_amount) <= 0:
            return jsonify(get_status_response(304))
        target_user_balance = users.find_one({"Username": target_user})["Balance"]
        new_target_user_balance = int(transfer_amount) + int(target_user_balance)
        my_present_balance = users.find_one({"Username": username})["Balance"]
        my_new_balance = int(my_present_balance) - int(transfer_amount)
        users.update_one({"Username": username}, {"$set": {"Balance": my_new_balance,}})
        users.update_one({"Username": target_user}, {"$set": {"Balance": new_target_user_balance,}})
        return jsonify({
            "Status code": 200,
            "Message": "Successfully transferred money"
        })

class CheckBalance(Resource):
    def post(self):
        get_posted_data = request.get_json()
        username = get_posted_data.get("username")
        password = get_posted_data.get("password")
        if not username or not password:
            return jsonify(get_status_response(306))
        if not check_existence(username):
            return jsonify(get_status_response(301))
        if not verify_password(username, password):
            return jsonify(get_status_response(302))
        my_balance = users.find_one({"Username": username})["Balance"]
        return jsonify({
            "Status code": 200,
            "Message1": "Your current balance is: $" + str(my_balance),
            "Message2": "you current loan is $" + str(users.find_one({"Username": username})["Loan"])
        })

class TakeLoan(Resource):
    def post(self):
        get_posted_data = request.get_json()
        username = get_posted_data.get("username")
        password = get_posted_data.get("password")
        take_loan_amount = get_posted_data.get("take_loan_amount")
        if not username or not password or not take_loan_amount:
            return jsonify(get_status_response(306))
        if not check_existence(username):
            return jsonify(get_status_response(301))
        if not verify_password(username, password):
            return jsonify(get_status_response(302))
        if int(take_loan_amount) <= 0:
            return jsonify(get_status_response(304))
        current_loan_amount = users.find_one({"Username": username})["Loan"]
        current_balance = users.find_one({"Username": username})["Balance"]
        new_loan_amount = int(take_loan_amount) + int(current_loan_amount)
        updated_balance = current_balance + take_loan_amount
        users.update_one({"Username": username},{"$set": {"Balance": updated_balance,}})
        users.update_one({"Username": username},{"$set": {"Loan": new_loan_amount}})
        return jsonify({
            "Status code": 200,
            "Message": "Loan Amount Taken. Your Total Loan Amount is: $" + str(new_loan_amount)
        })

class PayLoan(Resource):
    def post(self):
        get_posted_data = request.get_json()
        username = get_posted_data.get("username")
        password = get_posted_data.get("password")
        pay_loan = get_posted_data.get("pay_loan")
        if not username or not password or not pay_loan:
            return jsonify(get_status_response(306))
        if not check_existence(username):
            return jsonify(get_status_response(301))
        if not verify_password(username, password):
            return jsonify(get_status_response(302))
        if int(pay_loan) <= 0:
            return jsonify(get_status_response(304))
        current_balance = users.find_one({"Username": username})["Balance"]
        if current_balance < pay_loan:
            return jsonify(get_status_response(303))
        if current_balance == 0:
            return jsonify(get_status_response(308))
        current_loan_amount = users.find_one({"Username": username})["Loan"]
        if pay_loan > current_loan_amount:
            pay_loan = pay_loan - current_loan_amount
        new_balance = current_balance - pay_loan

        new_loan_amount = current_loan_amount - pay_loan
        users.update_one({"Username": username}, {"$set": {"Balance": new_balance}})
        users.update_one({"Username": username}, {"$set": {"Loan_Amount": new_loan_amount}})
        return jsonify({
            "Status code": 200,
            "Message1": "successfully loan paid $" + str(pay_loan),
            "Message2": "your loan amount is $" + str(new_loan_amount)
        })

api.add_resource(Register, '/register')
api.add_resource(Add, '/add')
api.add_resource(Transfer, '/transfer')
api.add_resource(CheckBalance, '/checkbalance')
api.add_resource(PayLoan, '/payloan')
api.add_resource(TakeLoan, '/loan')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)