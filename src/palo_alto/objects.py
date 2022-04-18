from firewall import Firewall, Server


class AddressObject:

    PREFIX_NAME = "splunk_"
    ENDPOINT = "/Objects/Addresses"

    def __init__(
        self,
        name: str,
        description: str,
        type: object,
        tags: list
    ) -> None:
        self.name = name
        self.description = description
        self.type = type
        self.tags = tags

    @property
    def full_name(self):
        return self.PREFIX_NAME + self.name

    def generate(self):
        return {
            "entry":[
                {
                    "@name": self.full_name,
                    "description": self.description,
                    "tag": {
                        "member": [tag.name for tag in self.tags]
                    },
                    **self.type.generate()
                }
            ]
        }


class Tag:
    """Tag"""

    COLOR = ()

    def __init__(
        self,
        name: str,
        color: str,
        commemts: str,
    ) -> None:
        self.name =name
        self._color = color
        self.commemts = commemts

    @property
    def color(self) -> str:
        return self.color

    @color.setter
    def color(self, value: str) -> None:
        self._color = value

    def generate(self) -> dict:
        pass


class IPNetmask:

    IPNETMASK = "ip-netmask"

    def __init__(self, value: str) -> str:
        self.value = value

    def generate(self) -> dict:
        return {self.IPNETMASK: self.value}

