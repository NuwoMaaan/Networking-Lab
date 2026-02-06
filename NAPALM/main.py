import napalm
from napalm.base.helpers import ConfigDict
from napalm.base import NetworkDriver
from DeviceConfig import DeviceConfig
from tabulate import tabulate
from yaml import safe_load

def load_devices_attr(file_path: str) -> dict[str, dict]:
    with open(file_path, 'r') as file:
        devices_attr = safe_load(file)
    return devices_attr

def initialize_devices(device_attr: dict) -> list[DeviceConfig]:
    device_configs = []
    print("Retrieving device connection configs...")
    for device in device_attr:
        print(device)
        device_config = DeviceConfig(
                node_name = device,
                OperatingSystem = device_attr[device]["os"],
                hostname = device_attr[device]["hostname"], 
                username = device_attr[device]["username"],
                password = device_attr[device]["password"],
                secret = device_attr[device]["secret"]
        )
        device_configs.append(device_config)
    print("Initialize device connections - Complete")
    return device_configs

def initialize_device_connections(devices: list[DeviceConfig]) -> dict[str, NetworkDriver]:
    connections = {}
    print("Initializing network drivers...")
    for device in devices:
        print(device.node_name, device.OperatingSystem)
        driver = napalm.get_network_driver(device.OperatingSystem)
        connections[device.node_name] = driver(
                hostname = device.hostname, 
                username = device.username, 
                password = device.password,
                optional_args = {"secret": device.secret,
                                 "read_timeout": 120
                },             
                timeout=60
        )
    print("Initializing drivers - Complete")
    return connections

def get_device_facts(devices: dict[str, NetworkDriver]) -> list[list[str]]:
    device_facts = [["hostname", "vendor", "model", "uptime", "serial_number"]]
    print("Retrieving device facts...")
    for device in devices:
        with devices[device] as d:
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
    for device in devices:
        with devices[device] as d:
            interfaces = d.get_interfaces()
            for interface in interfaces:
                device_interfaces.append([device,
                                        interface,
                                        interfaces[interface]["is_up"],
                                        interfaces[interface]["is_enabled"],
                                        interfaces[interface]["description"],
                                        interfaces[interface]["speed"],
                                        interfaces[interface]["mtu"],
                ])
    print("Getting interfaces - Complete")
    return device_interfaces


def get_device_configs(devices: dict[str, NetworkDriver]) -> ConfigDict:
    for device in devices:
        with devices[device] as d:
            configuration = d.get_config()
            return configuration["startup"], configuration["running"]
        
def command_test(devices: dict[str, NetworkDriver]) -> dict:
    for device in devices:
        with devices[device] as d:
            output = d.cli(["show vlan brief"])
            with open("vlan_brief.txt", "w") as f:
                f.write(str(output))


def print_to_terminal(device_facts: list[list[str]], device_interfaces: list[list[str]]) -> None:
    print()
    print(tabulate(device_facts, headers="firstrow"))
    print()
    print(tabulate(device_interfaces, headers="firstrow"))

def main():
    device_attr = load_devices_attr("devices.yaml")
    device_configs = initialize_devices(device_attr["devices"])
    devices = initialize_device_connections(device_configs)
    device_facts = get_device_facts(devices)
    device_interfaces = get_device_interfaces(devices)
    #startup_config, running_connfig = get_device_configs(devices)
    #command_test(devices)

    print_to_terminal(device_facts, device_interfaces)
    

if __name__ == "__main__":
    main()