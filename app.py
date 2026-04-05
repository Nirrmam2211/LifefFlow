from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json
from datetime import datetime
from flask_cors import CORS

# --- Basic Setup ---
app = Flask(__name__)
CORS(app)

# --- Database Connection ---
try:
    # This connects to your local MongoDB server and the 'lifeflow_db' database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["lifeflow_db"] # Using lifeflow_db as requested
    
    # Collection references
    donors_collection = db["donors"]
    banks_collection = db["blood_banks"]
    staff_collection = db["staff"]
    requests_collection = db["blood_requests"]
    inventory_collection = db["blood_inventory"]
    campaigns_collection = db["campaigns"]
    recipients_collection = db["recipients"]
    donations_collection = db["donations"]
    screening_collection = db["donation_screenings"]
    dispatch_collection = db["dispatches"]

    client.server_info()
    print("MongoDB connection successful.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

# --- DATABASE SEEDER ENDPOINT ---
@app.route('/api/seed-database', methods=['POST'])
def seed_database():
    """
    Clears all existing data and populates the database with the complete
    set of sample data from your original SQL file.
    """
    try:
        # 1. Clear all existing data
        print("Clearing existing data...")
        all_collections = [
            donors_collection, banks_collection, staff_collection, requests_collection,
            inventory_collection, campaigns_collection, recipients_collection,
            donations_collection, screening_collection, dispatch_collection
        ]
        for collection in all_collections:
            collection.delete_many({})
        
        # 2. Define the FULL sample data (translated from your SQL)
        print("Preparing to insert the full dataset...")
        
        banks_data = [
            {"bank_id": 1, "bank_name": "City Central Blood Bank", "address": "123 Health Ave", "city": "Lavale", "state": "Maharashtra", "contact_person": "Dr. Priya Sharma", "contact_phone": "9876543210"},
            {"bank_id": 2, "bank_name": "Community Blood Center", "address": "456 Life St", "city": "Pune", "state": "Maharashtra", "contact_person": "Mr. Raj Singh", "contact_phone": "9876543211"},
            {"bank_id": 3, "bank_name": "Lifeline Blood Services", "address": "789 Unity Blvd", "city": "Mumbai", "state": "Maharashtra", "contact_person": "Dr. Alok Gupta", "contact_phone": "9876543212"},
            {"bank_id": 4, "bank_name": "Sahyadri Blood Bank", "address": "101 Care Point", "city": "Nashik", "state": "Maharashtra", "contact_person": "Ms. Meena Kumari", "contact_phone": "9876543213"},
            {"bank_id": 5, "bank_name": "Regional Blood Center", "address": "212 Service Rd", "city": "Nagpur", "state": "Maharashtra", "contact_person": "Mr. Suresh Pawar", "contact_phone": "9876543214"}
        ]

        staff_data = [
            {"staff_id": 1, "bank_id": 1, "first_name": "Amit", "last_name": "Joshi", "role": "Administrator", "username": "amit.admin"},
            {"staff_id": 2, "bank_id": 1, "first_name": "Sunita", "last_name": "Patil", "role": "Nurse", "username": "sunita.nurse"},
            {"staff_id": 3, "bank_id": 2, "first_name": "Vikram", "last_name": "Rao", "role": "Technician", "username": "vikram.tech"},
            {"staff_id": 4, "bank_id": 1, "first_name": "Neha", "last_name": "Chavan", "role": "Technician", "username": "neha.tech"},
            {"staff_id": 5, "bank_id": 2, "first_name": "Rahul", "last_name": "Verma", "role": "Nurse", "username": "rahul.nurse"},
            {"staff_id": 6, "bank_id": 3, "first_name": "Sanjay", "last_name": "Shah", "role": "Administrator", "username": "sanjay.admin"},
            {"staff_id": 7, "bank_id": 3, "first_name": "Pooja", "last_name": "Iyer", "role": "Nurse", "username": "pooja.nurse"},
            {"staff_id": 8, "bank_id": 4, "first_name": "Deepak", "last_name": "More", "role": "Technician", "username": "deepak.tech"},
            {"staff_id": 9, "bank_id": 5, "first_name": "Anand", "last_name": "Kulkarni", "role": "Administrator", "username": "anand.admin"},
            {"staff_id": 10, "bank_id": 5, "first_name": "Leela", "last_name": "Menon", "role": "Nurse", "username": "leela.nurse"}
        ]
        
        donors_data = [
            {"donor_id": 1, "first_name": "Rohan", "last_name": "Mehta", "date_of_birth": datetime(1995, 8, 15), "blood_group": "O", "rh_factor": "+", "contact_number": "9988776655", "email": "rohan.mehta@email.com", "city": "Lavale", "state": "Maharashtra", "last_donation_date": datetime(2025, 1, 20)},
            {"donor_id": 2, "first_name": "Anjali", "last_name": "Desai", "date_of_birth": datetime(2000, 5, 22), "blood_group": "A", "rh_factor": "+", "contact_number": "9988776654", "email": "anjali.desai@email.com", "city": "Pune", "state": "Maharashtra", "last_donation_date": None},
            {"donor_id": 3, "first_name": "Karan", "last_name": "Verma", "date_of_birth": datetime(1992, 11, 30), "blood_group": "B", "rh_factor": "-", "contact_number": "9988776653", "email": "karan.verma@email.com", "city": "Lavale", "state": "Maharashtra", "last_donation_date": datetime(2024, 12, 10)},
            {"donor_id": 4, "first_name": "Aditi", "last_name": "Rane", "date_of_birth": datetime(1998, 2, 18), "blood_group": "AB", "rh_factor": "+", "contact_number": "9988776652", "email": "aditi.rane@email.com", "city": "Mumbai", "state": "Maharashtra", "last_donation_date": None},
            {"donor_id": 5, "first_name": "Vivek", "last_name": "Patel", "date_of_birth": datetime(1989, 7, 1), "blood_group": "O", "rh_factor": "-", "contact_number": "9988776651", "email": "vivek.patel@email.com", "city": "Nashik", "state": "Maharashtra", "last_donation_date": datetime(2025, 3, 15)},
        ]

        campaigns_data = [
            {"campaign_id": 1, "organizing_bank_id": 1, "campaign_name": "Lavale University Drive", "address": "Symbiosis University Campus", "city": "Lavale", "start_date": datetime(2025, 9, 15, 9, 0), "end_date": datetime(2025, 9, 15, 17, 0)},
            {"campaign_id": 2, "organizing_bank_id": 2, "campaign_name": "Pune City Marathon Camp", "address": "Deccan Gymkhana", "city": "Pune", "start_date": datetime(2025, 10, 5, 8, 0), "end_date": datetime(2025, 10, 5, 14, 0)},
            {"campaign_id": 3, "organizing_bank_id": 3, "campaign_name": "Corporate Wellness Week", "address": "BKC, Mumbai", "city": "Mumbai", "start_date": datetime(2026, 1, 18, 10, 0), "end_date": datetime(2026, 1, 22, 16, 0)},
            {"campaign_id": 4, "organizing_bank_id": 4, "campaign_name": "Nashik Industries Blood Drive", "address": "Ambad MIDC", "city": "Nashik", "start_date": datetime(2025, 11, 20, 9, 0), "end_date": datetime(2025, 11, 20, 17, 0)},
            {"campaign_id": 5, "organizing_bank_id": 5, "campaign_name": "Nagpur Community Health Fair", "address": "Kasturchand Park", "city": "Nagpur", "start_date": datetime(2025, 12, 1, 10, 0), "end_date": datetime(2025, 12, 1, 18, 0)}
        ]
        
        donations_data = [
            {"donation_id": 1, "donor_id": 1, "bank_id": 1, "campaign_id": None, "staff_id_processed": 2, "donation_date": datetime(2025, 9, 2, 18, 0), "quantity_ml": 450},
            {"donation_id": 2, "donor_id": 2, "bank_id": None, "campaign_id": 1, "staff_id_processed": 2, "donation_date": datetime(2025, 9, 15, 11, 30), "quantity_ml": 450},
            {"donation_id": 3, "donor_id": 3, "bank_id": 1, "campaign_id": None, "staff_id_processed": 4, "donation_date": datetime(2025, 9, 16, 10, 0), "quantity_ml": 450},
            {"donation_id": 4, "donor_id": 4, "bank_id": None, "campaign_id": 3, "staff_id_processed": 7, "donation_date": datetime(2026, 1, 18, 9, 30), "quantity_ml": 450},
            {"donation_id": 5, "donor_id": 5, "bank_id": None, "campaign_id": 4, "staff_id_processed": 8, "donation_date": datetime(2025, 11, 20, 11, 0), "quantity_ml": 450}
        ]
        
        screening_data = [
            {"screening_id": 1, "donation_id": 1, "technician_staff_id": 3, "screening_date": datetime(2025, 9, 2), "hemoglobin_level": 14.5, "blood_pressure": "120/80", "overall_result": "Pass"},
            {"screening_id": 2, "donation_id": 2, "technician_staff_id": 3, "screening_date": datetime(2025, 9, 15), "hemoglobin_level": 13.8, "blood_pressure": "110/70", "overall_result": "Pass"},
            {"screening_id": 3, "donation_id": 3, "technician_staff_id": 4, "screening_date": datetime(2025, 9, 16), "hemoglobin_level": 15.1, "blood_pressure": "125/85", "overall_result": "Pass"},
            {"screening_id": 4, "donation_id": 4, "technician_staff_id": 7, "screening_date": datetime(2026, 1, 18), "hemoglobin_level": 13.5, "blood_pressure": "115/75", "overall_result": "Pass"},
            {"screening_id": 5, "donation_id": 5, "technician_staff_id": 8, "screening_date": datetime(2025, 11, 20), "hemoglobin_level": 12.1, "blood_pressure": "130/90", "overall_result": "Fail"}
        ]

        inventory_data = [
            {"unit_id": 1, "donation_id": 1, "bank_id": 1, "blood_group": "O", "rh_factor": "+", "entry_date": datetime(2025, 9, 2), "expiry_date": datetime(2025, 10, 14), "status": "Dispatched"},
            {"unit_id": 2, "donation_id": 2, "bank_id": 1, "blood_group": "A", "rh_factor": "+", "entry_date": datetime(2025, 9, 15), "expiry_date": datetime(2025, 10, 27), "status": "Dispatched"},
            {"unit_id": 3, "donation_id": 3, "bank_id": 1, "blood_group": "B", "rh_factor": "-", "entry_date": datetime(2025, 9, 16), "expiry_date": datetime(2025, 10, 28), "status": "Dispatched"},
            {"unit_id": 4, "donation_id": 4, "bank_id": 3, "blood_group": "AB", "rh_factor": "+", "entry_date": datetime(2026, 1, 18), "expiry_date": datetime(2026, 3, 1), "status": "Available"}
        ]
        
        recipients_data = [
            {"recipient_id": 1, "first_name": "Priya", "last_name": "Kapoor", "date_of_birth": datetime(1985, 4, 10), "blood_group": "O", "rh_factor": "+", "hospital_name": "City Hospital"},
            {"recipient_id": 2, "first_name": "Arun", "last_name": "Kumar", "date_of_birth": datetime(1970, 2, 20), "blood_group": "A", "rh_factor": "+", "hospital_name": "Ruby Hall Clinic"},
            {"recipient_id": 3, "first_name": "Sneha", "last_name": "Jadhav", "date_of_birth": datetime(2005, 9, 5), "blood_group": "B", "rh_factor": "-", "hospital_name": "Jupiter Hospital"},
            {"recipient_id": 4, "first_name": "Mohan", "last_name": "Agrawal", "date_of_birth": datetime(1965, 12, 12), "blood_group": "O", "rh_factor": "+", "hospital_name": "City Hospital"}
        ]
        
        requests_data = [
            {"request_id": 1, "recipient_id": 1, "requesting_hospital": "City Hospital", "blood_group_requested": "O", "rh_factor_requested": "+", "quantity_units": 1, "priority": "Urgent", "status": "Fulfilled", "approved_by_staff_id": 1},
            {"request_id": 2, "recipient_id": 2, "requesting_hospital": "Ruby Hall Clinic", "blood_group_requested": "A", "rh_factor_requested": "+", "quantity_units": 2, "priority": "Normal", "status": "Fulfilled", "approved_by_staff_id": 1},
            {"request_id": 3, "recipient_id": 3, "requesting_hospital": "Jupiter Hospital", "blood_group_requested": "B", "rh_factor_requested": "-", "quantity_units": 1, "priority": "Urgent", "status": "Fulfilled", "approved_by_staff_id": 1},
            {"request_id": 4, "recipient_id": 4, "requesting_hospital": "City Hospital", "blood_group_requested": "O", "rh_factor_requested": "+", "quantity_units": 3, "priority": "Normal", "status": "Pending", "approved_by_staff_id": None}
        ]
        
        dispatch_data = [
            {"dispatch_id": 1, "request_id": 1, "unit_id": 1, "dispatched_by_staff_id": 1, "dispatch_time": datetime(2025, 9, 20, 14, 0), "receiving_hospital": "City Hospital"},
            {"dispatch_id": 2, "request_id": 2, "unit_id": 2, "dispatched_by_staff_id": 1, "dispatch_time": datetime(2025, 9, 22, 9, 0), "receiving_hospital": "Ruby Hall Clinic"},
            {"dispatch_id": 3, "request_id": 3, "unit_id": 3, "dispatched_by_staff_id": 1, "dispatch_time": datetime(2025, 9, 25, 11, 0), "receiving_hospital": "Jupiter Hospital"}
        ]

        # 3. Insert the data into the collections
        banks_collection.insert_many(banks_data)
        staff_collection.insert_many(staff_data)
        donors_collection.insert_many(donors_data)
        campaigns_collection.insert_many(campaigns_data)
        donations_collection.insert_many(donations_data)
        screening_collection.insert_many(screening_data)
        inventory_collection.insert_many(inventory_data)
        recipients_collection.insert_many(recipients_data)
        requests_collection.insert_many(requests_data)
        dispatch_collection.insert_many(dispatch_data)
        
        print("Full dataset insertion complete.")
        return jsonify({"message": "Database seeded successfully with the full dataset!"}), 201

    except Exception as e:
        print(f"Error during seeding: {e}")
        return jsonify({"error": str(e)}), 500

# --- Data Serialization Helper ---
def serialize_doc(doc):
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        elif isinstance(value, datetime):
            doc[key] = value.isoformat()
    return doc

# --- API Endpoints (Routes) ---

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the LifeFlow Backend API!"})

@app.route('/api/inventory/search', methods=['GET'])
def search_inventory():
    try:
        blood_group = request.args.get('blood_group')
        rh_factor = request.args.get('rh_factor')
        city = request.args.get('city')
        if not all([blood_group, rh_factor, city]):
            return jsonify({"error": "Missing required search parameters"}), 400
        pipeline = [
            {'$match': {'status': 'Available', 'blood_group': blood_group, 'rh_factor': rh_factor}},
            {'$lookup': {'from': 'blood_banks', 'localField': 'bank_id', 'foreignField': 'bank_id', 'as': 'bank_info'}},
            {'$unwind': '$bank_info'},
            {'$match': {'bank_info.city': {'$regex': f'^{city}$', '$options': 'i'}}},
            {'$project': {'_id': 0, 'unit_id': '$_id', 'expiry_date': 1, 'bank_name': '$bank_info.bank_name', 'bank_address': '$bank_info.address', 'bank_contact': '$bank_info.contact_phone'}}
        ]
        results = list(inventory_collection.aggregate(pipeline))
        return jsonify([serialize_doc(res) for res in results]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    try:
        stats = {
            "total_donors": donors_collection.count_documents({}),
            "units_in_stock": inventory_collection.count_documents({"status": "Available"}),
            "pending_requests": requests_collection.count_documents({"status": {"$ne": "Fulfilled"}}),
            "campaigns_active": campaigns_collection.count_documents({}) # Simplified for example
        }
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/register', methods=['POST'])
def register_donor():
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Request body must be valid JSON"}), 400

        required_fields = ['first_name', 'last_name', 'email', 'blood_group']
        missing_fields = [
            field for field in required_fields
            if field not in data or not str(data[field]).strip()
        ]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        if 'date_of_birth' in data and data['date_of_birth']:
            try:
                data['date_of_birth'] = datetime.fromisoformat(
                    data['date_of_birth'].replace('Z', '+00:00')
                )
            except ValueError:
                return jsonify({"error": "date_of_birth must be a valid ISO 8601 date"}), 400
        
        # Simple auto-increment for donor_id
        last_donor = donors_collection.find_one(sort=[("donor_id", -1)])
        data['donor_id'] = (last_donor['donor_id'] + 1) if last_donor else 1

        result = donors_collection.insert_one(data)
        # Use the custom donor_id, not the mongo _id
        return jsonify({"message": "Donor registered successfully!", "donor_id": data['donor_id']}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoints for fetching all data for dashboard tables
@app.route('/api/donors', methods=['GET'])
def get_donors():
    donors = list(donors_collection.find())
    return jsonify([serialize_doc(d) for d in donors]), 200

@app.route('/api/banks', methods=['GET'])
def get_banks():
    banks = list(banks_collection.find())
    return jsonify([serialize_doc(b) for b in banks]), 200

@app.route('/api/staff', methods=['GET'])
def get_staff():
    staff = list(staff_collection.find())
    return jsonify([serialize_doc(s) for s in staff]), 200

@app.route('/api/requests', methods=['GET'])
def get_requests():
    requests = list(requests_collection.find())
    return jsonify([serialize_doc(r) for r in requests]), 200

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    campaigns = list(campaigns_collection.find())
    return jsonify([serialize_doc(c) for c in campaigns]), 200

@app.route('/api/recipients', methods=['GET'])
def get_recipients():
    recipients = list(recipients_collection.find())
    return jsonify([serialize_doc(r) for r in recipients]), 200

@app.route('/api/donations', methods=['GET'])
def get_donations():
    donations = list(donations_collection.find())
    return jsonify([serialize_doc(d) for d in donations]), 200

@app.route('/api/inventory/summary', methods=['GET'])
def get_inventory_summary():
    try:
        pipeline = [
            {'$match': {'status': 'Available'}},
            {'$group': {'_id': {'blood_group': '$blood_group', 'rh_factor': '$rh_factor'}, 'total_units': {'$sum': 1}}},
            {'$sort': {'_id.blood_group': 1, '_id.rh_factor': -1}}
        ]
        summary = list(inventory_collection.aggregate(pipeline))
        labels = [f"{item['_id']['blood_group']}{item['_id']['rh_factor']}" for item in summary]
        data = [item['total_units'] for item in summary]
        return jsonify({"labels": labels, "data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Main execution block ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
