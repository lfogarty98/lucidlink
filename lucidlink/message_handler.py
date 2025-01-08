import cbor2
import uuid
import struct
from message_type import MessageType

class MessageHandler:
    def __init__(self, connection):
        self.connection = connection
        self.received_uuids = set()

    def parse_message(self, data):
        """Parse a message from the TCP stream."""
        # First 4 bytes are the length
        length = struct.unpack(">I", data[:4])[0]

        # Verify the length matches the data
        if length != len(data):
            raise ValueError(f"Message length mismatch: expected {length}, got {len(data)}")

        # Decode CBOR payload
        payload = cbor2.loads(data[4:])
        return payload

    def handle_message(self, payload):
        """Route the message to the appropriate handler."""
        message_type = payload.get("type")
        idem_uuid = payload.get("idem_uuid")

        # Deduplicate messages
        if idem_uuid in self.received_uuids:
            print(f"Duplicate message with UUID {idem_uuid}, ignoring.")
            return
        self.received_uuids.add(idem_uuid)

        # Route to handler
        if message_type == MessageType.VERSION_CHECK:
            self.handle_version_check(payload)
        elif message_type == MessageType.VERSION_REPLY:
            self.handle_version_reply(payload)
        elif message_type == MessageType.DEVICE_STATUS:
            self.handle_device_status(payload)
        elif message_type == MessageType.REQUEST_DEVICE_STATUS:
            self.handle_request_device_status(payload)
        elif message_type == MessageType.REQUEST_SYNCHRONIZATION:
            self.handle_request_synchronization(payload)
        elif message_type == MessageType.CHANGE_CONFIGURATION:
            self.handle_change_configuration(payload)
        else:
            print(f"Unknown message type: {message_type}")
    
    def send_message(self, message):
        """Encode and send a message over TCP."""
        cbor_payload = cbor2.dumps(message)
        length = struct.pack(">I", len(cbor_payload) + 4)  # Include the 4-byte length in total
        try:
            self.connection.sendall(length + cbor_payload)  # Send over the same connection
        except Exception as e:
            print(f"Failed to send message: {e}")


    ## Handlers for each message type ##
    def handle_version_check(self, payload):
        version = payload["payload"]["version"]
        print(f"Received Version Check: {version}")
        # Respond with a Version Reply
        self.send_message({
            "type": MessageType.VERSION_REPLY,
            "idem_uuid": str(uuid.uuid4()),
            "payload": {"version": "1.0.0"}
        })

    def handle_version_reply(self, payload):
        version = payload["payload"]["version"]
        print(f"Received Version Reply: {version}")

    def handle_device_status(self, payload):
        status = payload["payload"]
        print(f"Device Status: {status}")

    # TODO: move this to another class (server class probably), since this can only be sent by the host
    def handle_request_device_status(self, payload):
        print("Received Request Device Status")
        # Send a Device Status message
        self.send_message({
            "type": MessageType.DEVICE_STATUS,
            "idem_uuid": str(uuid.uuid4()),
            "payload": {
                "healthy": True,
                "battery_voltage": 3.8,
                "battery_soc": 0.8,
                "uptime": 9001,
                "cpu_load": 0.2,
                "min_free_heap": 51234,
                "rssi": "-70",
                "is_wifi6": True,
                "firmware_hash": "abc123"
            }
        })
        
    def handle_request_synchronization(self, payload):
        config = payload["payload"]["last_config"]
        schedule = payload["payload"]["schedule"]
        print(f'Received Request Synchronization: {config}, {schedule}')
        
    # TODO: move this to another class, since this can only be sent by the host
    def handle_change_configuration(self, payload):
        print(f"Received Change Configuration: {payload['payload']}")