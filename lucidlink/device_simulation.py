import socket
import cbor2
import struct
import uuid
from message_type import MessageType

def simulate_device(host='127.0.0.1', port=4572):
    try:
        # Connect to the host
        print(f"Connecting to {host}:{port}...")
        with socket.create_connection((host, port)) as device_socket:
            print("Connected to the host.")

            # Send a Version Check message
            message = {
                "type": MessageType.VERSION_CHECK,
                "idem_uuid": str(uuid.uuid4()),
                "payload": {"version": "1.0.0"}
            }
            cbor_payload = cbor2.dumps(message)
            length = struct.pack(">I", len(cbor_payload) + 4)  # Include the length
            device_socket.sendall(length + cbor_payload)

            # Receive response
            while True:
                length_data = device_socket.recv(4)
                if not length_data:
                    break
                
                response_length = struct.unpack(">I", length_data)[0]
                response_data = device_socket.recv(response_length - 4)
                response = cbor2.loads(response_data)
                print(f"Received response: {response}")
                break
            
            # response_length = struct.unpack(">I", device_socket.recv(4))[0]
            # response_data = device_socket.recv(response_length - 4)
            # response = cbor2.loads(response_data)
            # print(f"Received response: {response}")

            # Simulate disconnecting
            print("Disconnecting from the host.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    simulate_device()
