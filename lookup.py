from mac_vendor_lookup import MacLookup

def get_vendor(mac):
    try:
        return MacLookup().lookup(mac)
    except Exception:
        return "Unknown"

