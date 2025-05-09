import asyncio
from bleak import BleakScanner
from mqttportabo import send_payload
import time
from datetime import datetime

# Slovník známých UUID a jejich typů zařízení
KNOWN_DEVICE_UUIDS = {
    "0000180f-0000-1000-8000-00805f9b34fb": "Battery Service",
    "0000180a-0000-1000-8000-00805f9b34fb": "Device Information",
    "0000fe9f-0000-1000-8000-00805f9b34fb": "Google Fast Pair",
    "0000fd6f-0000-1000-8000-00805f9b34fb": "Windows Device",
    "9fa480e0-4967-4542-9390-d343dc5d04ae": "Apple Device",
    # Můžete přidat další UUID podle potřeby
}

def is_working_hours():
    """Kontroluje, zda je čas v pracovní době (7:00 - 19:00)"""
    current_hour = datetime.now().hour
    return 7 <= current_hour < 19

def get_device_type(uuids):
    """Zjistí typ zařízení podle UUID"""
    device_types = []
    for uuid in uuids:
        if uuid.lower() in KNOWN_DEVICE_UUIDS:
            device_types.append(KNOWN_DEVICE_UUIDS[uuid.lower()])
    return device_types if device_types else ["Unknown Device"]

def format_device_data(device):
    """Formátuje data ze zařízení do struktury pro MQTT"""
    uuids = device.metadata.get("uuids", [])
    return {
        "name": device.name or "Unknown",
        "mac": device.address,
        "rssi": device.rssi,
        "uuids": uuids,
        "device_types": get_device_type(uuids),
        "manufacturer_data": {
            str(k): v.hex() for k, v in device.metadata.get("manufacturer_data", {}).items()
        }
    }

async def scan_and_send():
    while True:  # Nekonečná smyčka pro kontinuální skenování
        if not is_working_hours():
            print("⏰ Mimo pracovní dobu (7:00-19:00), čekám...")
            await asyncio.sleep(30)  # Kontrola každých 30 sekund
            continue

        try:
            print("🔍 Spouštím BLE skenování...")
            devices = await BleakScanner.discover(timeout=10.0)  # 10 sekund skenování

            if not devices:
                print("❌ Nenalezena žádná BLE zařízení.")
                await asyncio.sleep(30)  # Čekání 30 sekund před dalším skenem
                continue

            print(f"✅ Nalezeno {len(devices)} zařízení")

            for device in devices:
                device_data = format_device_data(device)
                payload = {
                    "timestamp": int(time.time()),
                    "data": device_data
                }
                
                # Print device type information
                device_types = device_data["device_types"]
                print(f"📱 Zařízení {device.address} typu: {', '.join(device_types)}")

                try:
                    send_payload("ble_devices", payload)
                    print(f"📤 Odesláno: {device.address}")
                except Exception as e:
                    print(f"❌ Chyba při odesílání dat: {e}")

            await asyncio.sleep(30)  # Čekání 30 sekund před dalším skenem

        except Exception as e:
            print(f"❌ Chyba při skenování: {e}")
            await asyncio.sleep(5)  # Počkáme před dalším pokusem

if __name__ == "__main__":
    print("🚀 Spouštím BLE monitoring...")
    print("⏰ Pracovní doba: 7:00 - 19:00")
    asyncio.run(scan_and_send())
