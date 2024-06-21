import os
import subprocess


class OcctlUser:

    def __init__(self, username: str = None):
        self.username = username

    def add_or_update(self, password, group=None):
        command = f'/usr/bin/echo -e "{password}\n{password}\n" | sudo /usr/bin/ocpasswd'
        if group:
            command += f" -g {group}"
        command += f" -c /etc/ocserv/ocpasswd {self.username}"
        os.system(command)

    def lock(self, lock: bool):
        command = f'sudo /usr/bin/ocpasswd {"-l" if lock else "-u"} -c /etc/ocserv/ocpasswd {self.username}'
        os.system(command)

    def delete(self):
        command = f"sudo /usr/bin/ocpasswd  -c /etc/ocserv/ocpasswd -d {self.username}"
        os.system(command)

    def change_group(self, group: str = None):
        command = f"sudo /usr/bin/ocpasswd"
        if group:
            command += f" -g {group}"
        command += f" -c /etc/ocserv/ocpasswd {self.username}"
        os.system(command)

    def disconnect(self) -> str:
        p = subprocess.Popen(
            ("sudo", "/usr/bin/occtl", "disconnect", "user", f"{self.username}"),
            stdout=subprocess.PIPE,
        )
        output, err = p.communicate()
        if output:
            output = output.decode("utf-8")
            return output.strip()
        return None

    @staticmethod
    def sync():
        user_list = []
        with open("/etc/ocserv/ocpasswd", "r") as f:
            users = f.readlines()
        for user in users:
            user_split = user.rstrip().split(":")
            username, group, password = user_split[0], user_split[1], user_split[2]
            if group == "*":
                group = "defaults"
            user_list.append(
                {"username": username, "group": group, "lock": password.startswith("!")}
            )
        return user_list
