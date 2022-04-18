from firewall import Server, Firewall
from objects import AddressObject, IPNetmask, Tag


if __name__ == "__main__":

    hostname = "192.168.8.167"
    location = "vsys"
    vsys = "vsys1"
    api_key = "LUFRPT1KcDdNbXkyOTE0N001OTBYTUZvd3R5WUdBcDQ9bGExVEhTOVEwUkV1TWJEcG9SZXJaL016ZVhGeCsvSDhYZ0Q4eml1MHczNHJRZFBMVUc3cEQ5S2pYbHYwOWVlTQ=="


    ip = "192.168.51.3"

    server = Server(hostname)
    firewall = Firewall(server, location, api_key, vsys=vsys)

    ip_netmask = IPNetmask(ip)
    tag = Tag("splunk blocked", "blue", "hihi")
    address_object = AddressObject(ip, "testing", ip_netmask, [tag])
    output = firewall.create(address_object)
    print(output)
    commit = firewall.commit()

