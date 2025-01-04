from zeroconf import ServiceInfo, Zeroconf

# mDNS service class, for advertising a service on the network
class MDNSService:
    def __init__(self, service_name, service_type, port):
        self.zeroconf = Zeroconf()
        self.service_info = ServiceInfo(
            type_=service_type,
            name=service_name,
            port=port,
            properties={},
        )

    def start(self):
        self.zeroconf.register_service(self.service_info)
        print(f"mDNS service {self.service_info.name} started on port {self.service_info.port}")

    def stop(self):
        self.zeroconf.unregister_service(self.service_info)
        self.zeroconf.close()
        print("mDNS service stopped")
