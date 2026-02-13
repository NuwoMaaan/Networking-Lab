from DeviceConfig import DeviceConfig
from napalm.base import NetworkDriver
from yaml import safe_load
import napalm


def load_devices_attr(file_path: str) -> dict[str, dict]:
    with open(file_path, 'r') as file:
        devices_attr = safe_load(file)
    return devices_attr

def initialize_devices(device_attr: dict) -> list[DeviceConfig]:
    device_configs = []
    print("Retrieving device connection configs...")
    for device in device_attr:
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