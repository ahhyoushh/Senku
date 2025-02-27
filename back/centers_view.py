from flask import Blueprint, jsonify, request
from firebase_init import db
import json
from push_notifications import send_verification_email, serialiser, send_status_email
import threading

def async_send_email(email, status, item_name):
    thread = threading.Thread(target=send_status_email, args=(email,item_name, status))
    thread.start()

# ✅ Corrected Blueprint definition
centersbp = Blueprint("centersbp", __name__)

@centersbp.route('/send-verification', methods=["POST"])
def send_verification():
    data = request.json
    Name = data.get("Name")

    with open('places.geojson', 'r') as centers_json:
        centers = json.load(centers_json)

    email = None  # ✅ Initialize email to None

    for center in centers:
        if center.get("Name", "").lower() == Name.lower():  # ✅ Case insensitive check
            email = center.get("Email Address")
            break  # ✅ Stop once found

    if not email:
        return jsonify({"error": f"{Name} is not a center"}), 404  # ✅ Only return error if no match

    send_verification_email(email, Name)
    return jsonify({"message": "Email sent successfully!"}), 200

@centersbp.route('/verify/<token>', methods=["POST"])
def verify_email(token):
    try:
        email = serialiser.loads(token, salt="email-verification", max_age=1200)

        # 🔍 Check if center already exists in Firestore
        existing_centers = db.collection("centers").where("email_address", "==", email).stream()
        for center in existing_centers:
            center_data = center.to_dict()
            center_id = center.id
            return jsonify({"message": "Login successful!", "center_data": center_data, "centerId": center_id})

        # 🔍 Fetch center details from geojson
        with open('places.geojson', 'r') as centersbp_json:
            centers = json.load(centersbp_json)

        center_data = next((c for c in centers if c.get("Email Address") == email), None)

        if not center_data:
            return jsonify({"error": "Recycler not found"}), 404

        # ✅ Create new document since it does not exist
        center_ref = db.collection("centers").document()
        center_id = center_ref.id
        center_data["email_address"] = center_data.pop("Email Address")
        center_data["centerId"] = center_id
        center_ref.set(center_data)

        return jsonify({"message": "Login successful!", "center_data": center_data, "centerId": center_id})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@centersbp.route("/get-items", methods=["POST"])
def get_items():
    try:
        data = request.json
        centerId = data.get("centerId")

        if not centerId:
            return jsonify({"error": "centerId is required."}), 400

        try:
            center_ref = db.collection("centers").document(centerId).get()
            center_data = center_ref.to_dict()
            Name = center_data.get("Name")

        except Exception as e:
            return jsonify({"error": f"Error fetching center: {e}"}), 500

        item_ref = db.collection("items").where("nearest_center.Name", "==", Name).stream()
        items = []

        for doc in item_ref:
            item = doc.to_dict()
            item["itemId"] = doc.id
            items.append(item)

        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@centersbp.route("/delete-item", methods=["POST"])
def delete_item():
    try:
        data = request.json
        itemId = data.get("itemId")
        if not itemId:
            return jsonify({"error": "itemId missing"})
        item_ref = db.collection("items").document(itemId)
        item_doc = item_ref.get()
        item = item_doc.to_dict()

        if not item_doc.exists:
            return jsonify({'error': "Items not found!"})
        
        item_ref.delete()
        async_send_email(item["userEmail"], item["status"], item["itemName"])

        return jsonify({"message": "Item deleted succesfully!"}),200

    except Exception as e:
        return jsonify({"error": f"{e}"})
    
@centersbp.route("/approve", methods=["POST"])
def approve():
    try:
        data = request.json
        itemId = data.get("itemId")
        if not itemId:
            return jsonify({"error": "itemId or centerId needed"})
        
        item_ref = db.collection("items").document(itemId)
        item_doc = item_ref.get()
        item = item_doc.to_dict()

    

        item["status"] = "Approved"
        userEmail = item.get("userEmail")
        
        item_ref.set(item)

        if not item_doc.exists:
            return jsonify({"error": "Item does not exist"})
        async_send_email(userEmail, status=item["status"], item_name=item["itemName"])
        return jsonify({"message": 'Successfully approved!' })
    except Exception as e:
        return jsonify({"error": f"{e}"})
