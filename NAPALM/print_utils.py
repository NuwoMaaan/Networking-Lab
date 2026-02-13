import difflib
from tabulate import tabulate

def print_to_terminal(device_facts: list[list[str]], device_interfaces: list[list[str]]) -> None:
    print()
    print(tabulate(device_facts, headers="firstrow"))
    print()
    print(tabulate(device_interfaces, headers="firstrow"))

def print_diff(startup_config, running_config) -> None:
    diff = difflib.unified_diff(
    startup_config.splitlines(),
    running_config.splitlines(),
    fromfile="startup",
    tofile="running",
    lineterm=""
    )

    print("\n".join(diff))