import socket
import cbor2

def simulate_device(host='127.0.0.1', port=4572):
    try:
        # Connect to the host
        print(f"Connecting to {host}:{port}...")
        with socket.create_connection((host, port)) as sock:
            print("Connected to the host.")

            # Send a "ping" message
            ping_message = {"type": "ping"}
            print(f"Sending message: {ping_message}")
            sock.sendall(cbor2.dumps(ping_message))

            # Receive and decode the response
            response = sock.recv(1024)
            if response:
                decoded_response = cbor2.loads(response)
                print(f"Received response: {decoded_response}")

            # Simulate disconnecting
            print("Disconnecting from the host.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    simulate_device()
