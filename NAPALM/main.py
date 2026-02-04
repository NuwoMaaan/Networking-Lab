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
        # print(device_attr[device]["os"])
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

def initialize_drivers(devices: list) -> dict[str, NetworkDriver]:
    drivers = {}
    for device in devices:
        driver = napalm.get_network_driver(device.OperatingSystem)
        drivers[device.node_name] = driver(
                hostname = device.hostname, 
                username = device.username, 
                password = device.password,
                optional_args = {"secret": device.secret},
                timeout=60
        )
    #print(drivers[device.node_name].hostname)
    return drivers

def connect_to_devices(drivers: dict[str, NetworkDriver]) -> str:
    """Get facts test"""
    for d in drivers:
        with drivers[d] as device:
            print(device.get_facts())


def main():
    device_attr = load_devices_attr("devices.yaml")
    devices = initialize_devices(device_attr["devices"])
    drivers = initialize_drivers(devices)
    connect_to_devices(drivers)
    
    # with driver(**DSW1_settings, optional_args={"secret": "password",'read_timeout': 120}) as device:
    #     output.append(device.get_facts())
    #     for i in output:
    #         print(json.dumps(i, indent=4))

if __name__ == "__main__":
    main()