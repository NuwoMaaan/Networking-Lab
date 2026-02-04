import napalm
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
    return device_configs

def initialize_device_connections(devices: list[DeviceConfig]) -> dict[str, NetworkDriver]:
    connections = {}
    for device in devices:
        driver = napalm.get_network_driver(device.OperatingSystem)
        connections[device.node_name] = driver(
                hostname = device.hostname, 
                username = device.username, 
                password = device.password,
                optional_args = {"secret": device.secret},
                timeout=60
        )
    return connections

def connect_to_devices(devices: dict[str, NetworkDriver]) -> None:
    """Get facts test"""
    for d in devices:
        with devices[d] as device:
            print(device.get_facts())


def main():
    device_attr = load_devices_attr("devices.yaml")
    device_configs = initialize_devices(device_attr["devices"])
    devices = initialize_device_connections(device_configs)
    connect_to_devices(devices)

if __name__ == "__main__":
    main()