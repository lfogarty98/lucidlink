import socketserver
import cbor2
import struct
import threading
from message_handler import MessageHandler

# Global list of active connections, shared across two threads
active_connections = []

class LucidLinkTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Connection from: {self.client_address}")
        handler = MessageHandler(self.request)
        active_connections.append((self.request, self.client_address))
        try:
            while True:
                # Receive the message length
                length_data = self.request.recv(4)
                if not length_data:
                    break

                # Read the full message
                message_length = struct.unpack(">I", length_data)[0]
                data = self.request.recv(message_length - 4)

                # Parse and handle the message
                payload = handler.parse_message(length_data + data)
                handler.handle_message(payload)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            active_connections.pop()
            self.request.close()
            

class TCPServer:
    def __init__(self, host, port, handler=LucidLinkTCPHandler):
        self.handler = handler
        self.server = socketserver.ThreadingTCPServer((host, port), self.handler)
        self.server.allow_reuse_address = True

    def start(self):
        print(f"TCP server running on {self.server.server_address}")
        
        # Start the server in a separate thread
        server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        server_thread.start()
        
        # Simulate frontend sending a message to the device
        breakpoint()
        self.send_message_to_device({
            "type": 1234,
            "idem_uuid": 928357,
            "payload": {"version": "bonjour"}
        })

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        print("TCP server stopped")
    
    def send_message_to_device(self, message):
        """Send a message to a specific connection or broadcast to all."""
        cbor_payload = cbor2.dumps(message)
        length = struct.pack(">I", len(cbor_payload) + 4)  # Include the 4-byte length
        if self.active_connections:
                conn, addr = self.active_connections[0]
                conn.sendall(length + cbor_payload)
        else:
            print("No active connection found")