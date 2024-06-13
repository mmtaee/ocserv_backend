import json
import subprocess
from typing import Dict, List


class Occtl:

    @staticmethod
    def execute(command: list):
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        result, err = p.communicate()
        return result, err

    @property
    def online_users(self) -> List[Dict[str, str]]:
        command = [
            "sudo",
            "/usr/bin/occtl",
            "-j",
            "show",
            "users",
            "--output=json-pretty",
        ]
        result, err = self.execute(command)
        if result and len(result.decode("utf-8")) > 0:
            users = json.loads(result)
            return [{key.lower(): val for key, val in user.items()} for user in users]
        return []

    @property
    def ip_bans(self) -> List[Dict[str, str]]:
        command = ["sudo", "/usr/bin/occtl", "-j", "show", "ip", "bans"]
        bans, err = self.execute(command)
        if bans and len(bans.decode("utf-8")) > 0:
            bans = json.loads(bans)
            return [{key.lower(): val for key, val in ban.items()} for ban in bans]
        return []

    @property
    def iroutes(self) -> List[Dict[str, str]]:
        command = ["sudo", "/usr/bin/occtl", "-j", "show", "iroutes"]
        routes, err = self.execute(command)
        if routes and len(routes.decode("utf-8")) > 0:
            routes = json.loads(routes)
            return [{key.lower(): val for key, val in route.items()} for route in routes]
        return []

    @property
    def status(self) -> str:
        p = subprocess.Popen(
            ["sudo", "/usr/bin/occtl", "show", "status"], stdout=subprocess.PIPE
        )
        status_result, err = p.communicate()
        return status_result.decode("utf-8")
