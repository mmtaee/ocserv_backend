import os
from typing import AnyStr


class OcctlGroup:
    GROUP_DIR = "/etc/ocserv/groups"
    DEFAULT = "/etc/ocserv/defaults/group.conf"

    def __init__(self, group_name: str = None):
        self.group_name = group_name

    @staticmethod
    def _group_repr(file) -> dict[str, AnyStr]:
        config = {}
        for line in file.readlines():
            line = line.strip().split("=")
            key = line[0].replace("-", "_")
            value = line[1]
            match value:
                case "true":
                    value = True
                case "false":
                    value = False
            config[key] = line[1]
        return config

    @staticmethod
    def reload():
        command = f"sudo /usr/bin/occtl reload"
        os.system(command)

    def get_default(self) -> list[AnyStr]:
        with open(self.DEFAULT, "r") as f:
            return self._group_repr(f)

    def update_default(self, configs: list[AnyStr]):
        with open(self.DEFAULT, "w") as f:
            for config in configs:
                f.write(config + "\n")
        self.reload()

    def create_or_update_group(self, configs: list[AnyStr]):
        with open(f"{self.GROUP_DIR}/{self.group_name}", "w") as f:
            for config in configs:
                f.write(config + "\n")
        self.reload()

    def get_group(self):
        with open(f"{self.GROUP_DIR}/{self.group_name}", "r") as f:
            return self._group_repr(f)

    def delete_group(self):
        os.remove(f"{self.GROUP_DIR}/{self.group_name}")

    def group_exists(self) -> bool:
        return True if os.path.exists(f"{self.GROUP_DIR}/{self.group_name}") else False
