from napalm.base import NetworkDriver
from napalm.base.helpers import ConfigDict


def get_device_facts(devices: dict[str, NetworkDriver]) -> list[list[str]]:
    device_facts = [["hostname", "vendor", "model", "uptime", "serial_number"]]
    print("Retrieving device facts...")
    for nodename, driver in devices.items():
        with driver as d:
            facts = d.get_facts()
            device_facts.append([facts['hostname'],
                                 facts["vendor"],
                                 facts["model"],
                                 facts["uptime"],
                                 facts['serial_number']
            ])
    print("Getting facts - Complete")
    return device_facts

def get_device_interfaces(devices: dict[str, NetworkDriver]) -> list[list[str]]:
    device_interfaces = [["hostname", "interface","is_up", "is_enabled", "description", "speed", "mtu"]]
    print("Retrieving device interfaces...")
    for nodename, driver in devices.items():
        with driver as d:
            interfaces = d.get_interfaces()
            for interface in interfaces:
                device_interfaces.append([nodename,
                                        interface,
                                        interfaces[interface]["is_up"],
                                        interfaces[interface]["is_enabled"],
                                        interfaces[interface]["description"],
                                        interfaces[interface]["speed"],
                                        interfaces[interface]["mtu"],
                ])
    print("Getting interfaces - Complete")
    return device_interfaces


def get_device_configs(devices: dict[str, NetworkDriver]) -> tuple[ConfigDict, ConfigDict]:
    for _, driver in devices.items():
        with driver as d:
            configuration = d.get_config()
            return configuration["startup"], configuration["running"]