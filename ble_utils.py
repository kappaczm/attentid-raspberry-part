import asyncio
from bleak import BleakScanner

async def get_nearby_mac_addresses():
    """Retrieve a list of nearby MAC addresses using BLE scanning."""
    try:
        devices = await BleakScanner.discover(timeout=5.0)
        macs = [device.address for device in devices]
        print(f"Nearby MAC addresses: {macs}")  # Debugging log
        return macs
    except Exception as e:
        print(f"Error during BLE scanning: {e}")
        return []