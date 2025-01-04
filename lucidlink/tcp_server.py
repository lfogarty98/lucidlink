import socketserver
import cbor2
import struct
from message_handler import MessageHandler

class LucidLinkTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Connection from: {self.client_address}")
        handler = MessageHandler(self.request)
        while True:
            try:
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
                break

class TCPServer:
    def __init__(self, host, port):
        self.server = socketserver.ThreadingTCPServer((host, port), LucidLinkTCPHandler)
        self.server.allow_reuse_address = True

    def start(self):
        print(f"TCP server running on {self.server.server_address}")
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        print("TCP server stopped")
