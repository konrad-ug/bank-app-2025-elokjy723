from flask import Flask, request, jsonify
from src.account import Account, AccountRegistry

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    if not data or 'pesel' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    pesel = data.get("pesel")

    if registry.search_account_pesel(pesel):
        return jsonify({"message": "Account with this pesel already exists"}), 409

    name = data.get("name")
    surname = data.get("surname")

    account = Account(name, surname, pesel)
    registry.add_account(account)

    return jsonify({"message": "Account created", "account": {"name": name, "surname": surname, "pesel": pesel}}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.all_accounts()
    accounts_data = [
        {"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance} 
        for acc in accounts
    ]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    count = registry.number_of_accounts()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.search_account_pesel(pesel)
    if account:
        return jsonify({
            "name": account.first_name,
            "surname": account.last_name,
            "pesel": account.pesel,
            "balance": account.balance
        }), 200
    else:
        return jsonify({"message": "Account not found"}), 404

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    account = registry.search_account_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    data = request.get_json()
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
        
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.search_account_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    registry.accounts.remove(account)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def make_transfer(pesel):
    account = registry.search_account_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404

    data = request.get_json()
    amount = data.get("amount")
    transfer_type = data.get("type")

    if transfer_type == "incoming":
        account.transfer_incoming(amount)
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200

    elif transfer_type == "outgoing":
        result = account.transfer_outgoing(amount)
        if result:
            return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
        else:
            return jsonify({"message": "Niewystarczające środki"}), 422

    elif transfer_type == "express":
        result = account.express_transfer(amount)
        if result:
            return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
        else:
            return jsonify({"message": "Niewystarczające środki"}), 422

    else:
        return jsonify({"message": "Invalid transfer type"}), 400

if __name__ == '__main__':
    app.run(debug=True)