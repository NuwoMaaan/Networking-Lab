from dataclasses import dataclass

@dataclass
class DeviceConfig():
    def __init__(self, OperatingSystem, node_name, hostname, username, password, secret=None):
        self.node_name: str = node_name
        self.OperatingSystem: str = OperatingSystem
        self.hostname: int = hostname
        self.username: str = username
        self.password: str = password
        self.secret: str | None = secret
