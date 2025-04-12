# Arrrrr Dino Project

This project involves setting up a TLS server and client for secure communication, reading UID from RFID tags, and integrating with Firebase for real-time updates.

## Project Structure

- `tls_server.py`: Contains the TLS server implementation.
- `tls_client.py`: Contains the TLS client implementation.
- `servercode1.py`: Reads UID from an Arduino and sends it over TLS.
- `servercode.py`: Basic TLS server example.
- `reading_uid_from_rfid_tag.ino`: Arduino code for reading UID from RFID tags.
- `readfromfb.py`: Reads data from Firebase Firestore.
- `server.key`: TLS server private key.
- `server.crt`: TLS server certificate.

## Setup

### Prerequisites

- Python 3.x
- Arduino IDE
- Firebase account and Firestore database
- Required Python packages: `firebase-admin`, `cryptography`, `tinyec`, `secrets`, `hashlib`, `hmac`, `socket`, `ssl`

### Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd arrrrr-dino
    ```

2. Install the required Python packages:
    ```sh
    pip install firebase-admin cryptography tinyec
    ```

3. Upload the `reading_uid_from_rfid_tag.ino` code to your Arduino.

4. Set up Firebase Firestore and download the service account credentials JSON file. Place it in the project directory.

## Usage

### Running the TLS Server

1. Run the TLS server:
    ```sh
    python tls_server.py
    ```

### Running the TLS Client

1. Run the TLS client:
    ```sh
    python tls_client.py
    ```

### Reading UID from Arduino

1. Run the script to read UID from Arduino:
    ```sh
    python servercode1.py
    ```

### Listening for Firebase Changes

1. Run the script to listen for changes in Firebase Firestore:
    ```sh
    python readfromfb.py
    ```

## License

This project is licensed under the MIT License.
