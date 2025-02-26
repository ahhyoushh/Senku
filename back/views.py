from flask import Blueprint, jsonify, request   
from functions import generate_metadata,nearest_center
from firebase_init import db
from push_notifications import send_status_email, send_newItem_email
import threading

views = Blueprint(__name__, "views")

"""
@views.route('/login-gen', methods=["POST"])
def generate_otp():
    data = request.json
    phone_no = data.get("phone_number")
    otp = gen_otp(phone_number=phone_no)

    return jsonify({"Message": "Otp has been sent", "otp": otp})

@views.route('/login-verify', methods=["POST"])
def verify_otp_r():
    data = request.json
    otp_r = data.get("otp_entered")
    print(otp_r)
    phone_number = data.get("phone_number")

    if verify_otp(otp_r):
        
        userId = get_create_userId(phone_no=phone_number)
        return jsonify({"message": "created successfully", "userId": userId})
    else:
        return jsonify({"message": "INVALID OTP"})
            
"""

"""@views.route("/login", methods=["POST"])
def verify_login():
    data = request.json
    token = data.get("token")  
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token["userId"]
        email = decoded_token.get("email", "")
        
        user_ref = db.collection("users").document(user_id)
        if not user_ref.get().exists:
            user_ref.set({"email": email, "role": "user"})

        return jsonify({"message": "Loging Sucessful", "userId": user_id, "email": email})
    except Exception as e:
        return jsonify({"message": "Login failed", "erorr": str(e)})"""


def async_send_email(email, status, item_name):
    thread = threading.Thread(target=send_status_email, args=(email,status,item_name))
    thread.start()

def async_send_newItem_email(item_count, item_name, center_email):
    thread = threading.Thread(target=send_newItem_email, args=(item_count,item_name, center_email))
    thread.start()

@views.route("/get-items", methods=["POST"])
def get_items():
    try:
        data = request.json
        userId = data["userId"]
        if not userId:
            return jsonify({"error": "userId is required."})
        
        item_ref = db.collection("items").where("userId", '==', userId).stream()
        items = []

        for doc in item_ref:
            item = doc.to_dict()
            item["itemId"] = doc.id
            items.append(item)

        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": f'{e}'}), 500

@views.route("/list-item", methods=["POST"])
def list_item():
    try:
        data = request.json
        Email = data.get("userEmail")
        itemName = data.get("itemName")
        refurbishable = data.get("refurbishable", False)
        itemCount = data.get("itemCount")
        userId = data.get("userId")
        userCoordinates = data.get("userCoordinates")

        if not all([itemName, userId]):
            return jsonify({"error": "Missing itemName or userId"}), 400

        metadata = generate_metadata(itemName)
        center = nearest_center(userCoordinates, refurbishable)
        print(center)
        item_ref = db.collection("items").document()
        item_id = item_ref.id
        
        item_data = {
            "itemId": item_id,
            "userId": userId,
            "userEmail": Email,
            "itemName": itemName,
            "itemCount": itemCount,
            "refurbishable": refurbishable,
            "status": "Listed",
            "nearest_center": center,
            "metadata" : metadata
        }
        item_ref.set(item_data)
        async_send_email(item_data["userEmail"], status=item_data["status"], itemName=item_data["itemName"])

        #notify_recycler()
        centerEmail = center["Email Address"]
        async_send_newItem_email(itemCount=itemCount, itemName=itemName, center_email=centerEmail)
        return jsonify({"message": "Item listed successfully", "itemId": item_id, "metadata": metadata, "refurbishable": refurbishable,"nearest_recycler":center })
    except Exception as e:
        return jsonify({"error": f"{e}"})


@views.route("/delete-item", methods=["POST"])
def delete_item():
    try:
        data = request.json
        userId = data.get("userId")
        itemId = data.get("itemId")
        if not itemId or not userId:
            return jsonify({"error": "itemId or userId missing"})
        item_ref = db.collection("items").document(itemId)
        item_doc = item_ref.get()

        if not item_doc.exists:
            return jsonify({'error': "Items not found!"})
        
        item_data = item_doc.to_dict()
        if item_data.get("userId") != userId:
            return jsonify({"error": "You do not own this item."})
        
        item_ref.delete()

        return jsonify({"message": "Item deleted succesfully!"}),200

    except Exception as e:
        return jsonify({"error": f"{e}"})