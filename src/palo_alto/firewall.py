import requests


class Server:
    """Server Object using for connect to host"""

    URI_PATTERN = "{schema}://{hostname}:{port}"
    API_PATH_PATTERN = "/restapi/{version}"

    def __init__(
        self,
        hostname: str,
        port: bool = 443,
        timeout: int = 30,
        verify: bool = False,
        is_https: bool = True,
        version: str = "v10.0"
    ) -> None:
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self.verify = verify
        self.is_https = is_https
        self.version = version

    @property
    def url(self) -> str:
        api_path = self.API_PATH_PATTERN.format(version=self.version)
        return self.uri + api_path

    @property
    def uri(self) -> str: 
        uri = self.URI_PATTERN.format(
            schema="https" if self.is_https else "http",
            hostname=self.hostname,
            port=self.port,
        )
        return uri


class Firewall:
    """Palo Alto Network Firewall"""

    SHARED_LOCATION = "shared"
    VSYS_LOCATION = "vsys"
    LOCATION = ("shared", "vsys")

    def __init__(
        self,
        server: object,
        location: str,
        api_key: str,
        **kwargs,
    ):
        self.server = server
        self._location = location
        self._api_key = api_key
        self._vsys = kwargs.pop("vsys", None)

        self._headers = {
            "X-PAN-KEY": self._api_key
        }

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str) -> None:
        if value in self.LOCATION:
            self._location = value
        else:
            raise ValueError(f"Location must in {self.LOCATION}")

    @property
    def vsys(self) -> str:
        return self._vsys

    @vsys.setter
    def vsys(self, value: str) -> None:
        if not self.is_shared():
            self._vsys = value
        else:
            raise ValueError("Location must have value = vsys")

    def is_shared(self) -> bool:
        if self._location == self.SHARED_LOCATION:
            return True
        else:
            return False

    def generate_params(self) -> dict:
        params = {
            "location": self.location,
        }

        if not self.is_shared():
            params["vsys"] = self._vsys

        return params

    def create(self, obj: object) -> str:

        url = self.server.url + obj.ENDPOINT
        data = obj.generate()

        params = self.generate_params()
        params["name"] = obj.full_name

        resp = requests.post(
            url=url,
            headers=self._headers,
            params=params,
            json=(data),
            timeout=self.server.timeout,
            verify=self.server.verify
        )

        return resp.json()

    def delete(self, obj) -> str:
        url = self.server.url + obj.ENDPOINT

        params = self.generate_params()
        params["name"] = obj.full_name

        resp = requests.delete(
            url=url,
            headers=self._headers,
            params=params,
            timeout=self.server.timeout,
            verify=self.server.verify
        )

        return resp.json()


    def edit(self, obj) -> str:
        url = self.server.url + obj.ENDPOINT

        params = self.generate_params()
        params["name"] = obj.full_name

        resp = requests.put(
            url=url,
            headers=self._headers,
            params=params,
            timeout=self.server.timeout,
            verify=self.server.verify
        )

        return resp.json()

    def commit(self) -> str:
        params = {
            "type": "commit",
            "cmd": "<commit></commit>",
        }
        url = self.server.uri + "/api"

        resp = requests.get(
            url=url,
            headers=self._headers,
            params=params,
            timeout=self.server.timeout,
            verify=self.server.verify
        )

        return resp.text

