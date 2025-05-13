import asyncio
import re
from porovnani import get_nearby_mac_addresses

def handle_incoming_message(message):
    """
    Handle an incoming message by extracting the MAC address,
    comparing it with nearby MAC addresses, and outputting the result.
    """
    try:
        # Extract MAC address from the message
        mac_address = message.get("mac")
        if not mac_address:
            print("No MAC address found in the message.")
            return

        # Retrieve nearby MAC addresses
        nearby_macs = asyncio.run(get_nearby_mac_addresses())

        # Normalize MAC address formats
        def normalize_mac(mac):
            return re.sub(r'[^A-Fa-f0-9]', '', mac).upper()

        normalized_mac = normalize_mac(mac_address)
        normalized_nearby_macs = [normalize_mac(mac) for mac in nearby_macs]

        # Compare the MAC address with the nearby list
        if normalized_mac in normalized_nearby_macs:
            print(f"MAC address {mac_address} is nearby.")
        else:
            print(f"MAC address {mac_address} is not nearby.")
    except Exception as e:
        print(f"Error handling the message: {e}")