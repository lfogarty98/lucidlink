import socketserver
import cbor2
import struct
import uuid
import threading
import time
from message_handler import MessageHandler
from message_type import MessageType


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
        print("Simulating frontend sending a message to the device...")
        breakpoint()
        self.send_hard_error("Critical error occurred") # Send a Hard Error message, for example
        # self.send_version_check() # Send a Version Check message, for example

    def stop(self):
        print("TCP server stopped")
        self.server.shutdown()
        self.server.server_close()
    
    ## Frontend message senders ## 
    
    def send_message_to_device(self, message):
        """Send a message to a specific connection or broadcast to all."""
        cbor_payload = cbor2.dumps(message)
        length = struct.pack(">I", len(cbor_payload) + 4)  # Include the 4-byte length
        if active_connections:
                conn, addr = active_connections[0]
                conn.sendall(length + cbor_payload)
        else:
            print("No active connection found")
            
    def send_version_check(self):
        self.send_message_to_device({
            "type": MessageType.VERSION_CHECK,
            "idem_uuid": str(uuid.uuid4()),
            "payload": {
                "version": "1.0.0",
                "protocol": 1,
            }
        })
    
    def send_request_device_status(self):
        self.send_message_to_device({
            "type": MessageType.REQUEST_DEVICE_STATUS,
            "idem_uuid": str(uuid.uuid4()),
            "payload": {}
        })
    
    def send_request_synchronization(self):
        # TODO: Implement
        pass
    
    def send_change_configuration(self):
        # TODO: Implement
        pass
    
    def send_soft_error(self, error_msg):
        self.send_message_to_device({
            "type": MessageType.SOFT_ERROR,
            "idem_uuid": str(uuid.uuid4()),
            "payload": {
                "msg": error_msg,
            }
        })
        
    def send_hard_error(self, error_msg):
        self.send_message_to_device({
            "type": MessageType.HARD_ERROR,
            "idem_uuid": str(uuid.uuid4()),
            "payload": {
                "msg": error_msg,
            }
        })
        print("Hard error sent")
        self.stop() # Stop the server after sending a hard error