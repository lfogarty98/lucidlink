import socketserver
import cbor2
from message_handler import MessageHandler

class LucidLinkTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Connection from: {self.client_address}")
        handler = MessageHandler()
        while True:
            try:
                # Read data from the device
                data = self.request.recv(1024)
                if not data:
                    break
                
                # Decode the CBOR message
                message = cbor2.loads(data)
                print(f"Received: {message}")
                # Example response, TODO: Implement message handler
                response = {"status": "OK"}
                self.request.sendall(cbor2.dumps(response))
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
