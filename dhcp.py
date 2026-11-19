import requests
import os
import dotenv
dotenv.load_dotenv()

requests.packages.urllib3.disable_warnings()

def get_leases():
    leases = {}

    url = f"https://{os.getenv('DHCP_SERVER')}{os.getenv('DHCP_ENDPOINT')}"

    response = requests.get(url, verify=False, headers={"Authorization": f"Bearer {os.getenv('DHCP_TOKEN')}"})

    if response.status_code == 200:
        data = response.json()
        for lease in data.get("results", []):
            ip = lease.get("ip")
            mac = lease.get("mac")
            hostname = lease.get("hostname")
            if ip and mac:
                leases[ip] = {"mac": mac, "hostname": hostname}
    else:
        print(f"Failed to fetch DHCP leases: {response.status_code}")

    return leases

def get_pool():
    pool = {}
    url = f"https://{os.getenv('DHCP_SERVER')}{os.getenv('DHCP_POOL_ENDPOINT')}"

    response = requests.get(url, verify=False, headers={"Authorization": f"Bearer {os.getenv('DHCP_TOKEN')}"})

    if response.status_code == 200:
        data = response.json()
        for pool_entry in data.get("results", []):
            ip = pool_entry.get("ip")
            if ip:
                pool[ip] = True
    else:
        print(f"Failed to fetch DHCP pool: {response.status_code}")

    return pool

def get_active():
    active = {}

    url = f"https://{os.getenv('DHCP_SERVER')}{os.getenv('DHCP_ARP_ENDPOINT')}"

    response = requests.get(url, verify=False, headers={"Authorization": f"Bearer {os.getenv('DHCP_TOKEN')}"})

    if response.status_code == 200:
        data = response.json()
        for arp_entry in data.get("results", []):
            ip = arp_entry.get("ip")
            mac = arp_entry.get("mac")
            if ip and mac:
                active[ip] = {"mac": mac}
    else:
        print(f"Failed to fetch active ARP entries: {response.status_code}")

    return active