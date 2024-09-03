import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
cred = credentials.Certificate(r'C:/Users/shail/rfid-db-5d32b-firebase-adminsdk-dbval-d4136a83f1.json')

firebase_admin.initialize_app(cred)
db = firestore.client()

def on_snapshot(col_snapshot, changes, read_time):
    """Callback function to handle changes to the Firestore collection."""
    for doc in col_snapshot:
        data = doc.to_dict()
        uid = data.get('uid', 'N/A')
        timestamp = data.get('timestamp', 'N/A')
        print(f"Latest UID: {uid} at {timestamp}")

def main():
    print("Listening for changes in Firebase...")
    # Set up a real-time listener for the 'rfid_data' collection
    col_ref = db.collection('rfid_data')
    query = col_ref.order_by('timestamp', direction=firestore.Query.DESCENDING)
    query.on_snapshot(on_snapshot)

    # Keep the script running indefinitely
    import time
    while True:
        time.sleep(1)  # Sleep to prevent the script from exiting

if __name__ == "__main__":
    main()
