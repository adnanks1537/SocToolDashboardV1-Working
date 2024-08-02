import json
import time
from scapy.all import sniff, Raw
from pymongo import MongoClient
from flask import Flask, jsonify
from urllib.parse import quote_plus

# Replace these with your actual username and password
username = "adnankstheredteamlabs"
password = "Adnan@66202"
# Make sure to replace with your cluster name and database name
cluster_name = "cluster0"
database_name = "network_packets"
import json
import time
from scapy.all import sniff, Raw
from pymongo import MongoClient
from flask import Flask, jsonify
from urllib.parse import quote_plus

# Replace these with your actual username and password
username = "adnankstheredteamlabs"
password = "Adnan@66202"
# Make sure to replace with your cluster name and database name
cluster_name = "cluster0"
database_name = "network_packets"

# URL-encode the username and password
username_encoded = quote_plus(username)
password_encoded = quote_plus(password)

# Construct the MongoDB connection URI
MONGO_URI = f"mongodb+srv://{username_encoded}:{password_encoded}@{cluster_name}.qrppz7h.mongodb.net/{database_name}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client[database_name]
collection = db['packets']

# Flask app to provide API endpoints
app = Flask(__name__)

def packet_callback(packet):
    packet_dict = {
        'timestamp': time.time(),
        'src_ip': packet[1].src,
        'dst_ip': packet[1].dst,
        'protocol': packet[2].name,
        'length': len(packet),
        'raw_data': bytes(packet).hex()
    }

    if packet.haslayer(Raw):
        packet_dict['payload'] = packet[Raw].load.decode(errors='ignore')

    collection.insert_one(packet_dict)
    print(f"Packet captured and stored: {packet_dict}")

# Sniffing function
def start_sniffing():
    sniff(prn=packet_callback, store=0)

# API endpoint to get packet data
@app.route('/api/packets', methods=['GET'])
def get_packets():
    packets = list(collection.find().sort("timestamp", -1).limit(10))
    for packet in packets:
        packet['_id'] = str(packet['_id'])
    return jsonify(packets)

if __name__ == "__main__":
    from multiprocessing import Process
    p = Process(target=start_sniffing)
    p.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
    p.join()

# URL-encode the username and password
username_encoded = quote_plus(username)
password_encoded = quote_plus(password)

# Construct the MongoDB connection URI
MONGO_URI = f"mongodb+srv://{username_encoded}:{password_encoded}@{cluster_name}.qrppz7h.mongodb.net/{database_name}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client[database_name]
collection = db['packets']

# Flask app to provide API endpoints
app = Flask(__name__)

def packet_callback(packet):
    packet_dict = {
        'timestamp': time.time(),
        'src_ip': packet[1].src,
        'dst_ip': packet[1].dst,
        'protocol': packet[2].name,
        'length': len(packet),
        'raw_data': bytes(packet).hex()
    }

    if packet.haslayer(Raw):
        packet_dict['payload'] = packet[Raw].load.decode(errors='ignore')

    collection.insert_one(packet_dict)
    print(f"Packet captured and stored: {packet_dict}")

# Sniffing function
def start_sniffing():
    sniff(prn=packet_callback, store=0)

# API endpoint to get packet data
@app.route('/api/packets', methods=['GET'])
def get_packets():
    packets = list(collection.find().sort("timestamp", -1).limit(10))
    for packet in packets:
        packet['_id'] = str(packet['_id'])
    return jsonify(packets)

if __name__ == "__main__":
    from multiprocessing import Process
    p = Process(target=start_sniffing)
    p.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
    p.join()
