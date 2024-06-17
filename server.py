from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

current_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(current_dir, 'server_received')
PORT = 9999
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

messages = []

@app.route('/message', methods=['POST'])
def receive_message():
    if 'file' in request.files:
        file = request.files['file']
        filename = os.path.join(UPLOAD_FOLDER, file.filename.split('/')[-1])

        try:
            file.save(filename)
            message = f'File {filename} received'
        except Exception as e:
            message = f'Failed to save file: {e}'
        print(message)
    else:
        data = request.json
        message = data.get('message')
    
    client_ip = request.environ.get('REMOTE_ADDR')
    client_port = request.environ.get('REMOTE_PORT')
    server_ip = request.host.split(':')[0]
    server_port = PORT

    headers = {key: value for key, value in request.headers.items()}

    log_entry = {
        "source": f"{client_ip}:{client_port}",
        "destination": f"{server_ip}:{server_port}",
        "data": message,
        "headers": headers
    }

    # print(log_entry)
    messages.append(log_entry)
    return jsonify({"response": f"[Received] {message}", "log": log_entry}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
