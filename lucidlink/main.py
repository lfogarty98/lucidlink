from mdns_service import MDNSService
from tcp_server import TCPServer

def main():
    # Initialize mDNS service
    mdns = MDNSService(service_name="LucidLink Host._lucidlink._tcp.local.",
                       service_type="_lucidlink._tcp.local.",
                       port=4572)

    # Start the mDNS service
    mdns.start()

    # Initialize and start the TCP server
    tcp_server = TCPServer(host="0.0.0.0", port=4572)
    try:
        tcp_server.start()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        # Clean up
        tcp_server.stop()
        mdns.stop()

if __name__ == "__main__":
    main()
