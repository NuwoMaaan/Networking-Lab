from connection import load_devices_attr, initialize_device_connections, initialize_devices
from get_functions import get_device_interfaces, get_device_facts, get_device_configs
from print_utils import print_diff, print_to_terminal
    

def main():
    device_attr = load_devices_attr("devices.yaml")
    device_configs = initialize_devices(device_attr["devices"])
    devices = initialize_device_connections(device_configs)
    device_facts = get_device_facts(devices)
    device_interfaces = get_device_interfaces(devices)
    startup_config, running_connfig = get_device_configs(devices)
    #command_test(devices)
    print_diff(startup_config, running_connfig)
    print_to_terminal(device_facts, device_interfaces)
    

if __name__ == "__main__":
    main()



# def command_test(devices: dict[str, NetworkDriver]) -> dict:
#     for device in devices:
#         with devices[device] as d:
#             output = d.cli(["show vlan brief"])
#             with open("vlan_brief.txt", "w") as f:
#                 f.write(str(output))