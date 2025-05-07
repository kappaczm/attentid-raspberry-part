import asyncio
from bleak import BleakScanner

def format_manufacturer_data(mdata):
    if not mdata:
        return "None"
    return ", ".join(f"ID {k}: {v.hex()}" for k, v in mdata.items())

def format_uuids(uuids):
    if not uuids:
        return "None"
    return ", ".join(uuids)

async def scan_devices():
    print("🔍 Spoustím BLE skenování...")
    devices = await BleakScanner.discover()

    if not devices:
        print("❌ Nenašel jsem žádná BLE zařízení.")
        return

    print(f"✅ Nalezeno {len(devices)} zařízení:\n")
    
    for d in devices:
        name = d.name or "Neznámé zařízení"
        address = d.address
        rssi = d.rssi

        mdata = d.metadata.get("manufacturer_data", {})
        uuids = d.metadata.get("uuids", [])

        print(f"📱 Název:        {name}")
        print(f"🔗 Adresa (MAC): {address}")
        print(f"📶 RSSI:         {rssi} dBm")
        print(f"🧬 UUIDs:        {format_uuids(uuids)}")
        print(f"🏭 Výrobce data: {format_manufacturer_data(mdata)}")
        print("-" * 50)

asyncio.run(scan_devices())
