import requests
import os
import dotenv
dotenv.load_dotenv()

requests.packages.urllib3.disable_warnings()

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

for i in leases.keys():
    print(f"IP: {i}, MAC: {leases[i]['mac']}, Hostname: {leases[i]['hostname']}")