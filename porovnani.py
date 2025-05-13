from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

class DeviceComparator:
    def __init__(self, match_window_seconds=30):
        self.source1_devices = defaultdict(list)  # MAC -> [(timestamp, data)]
        self.source2_devices = defaultdict(list)  # MAC -> [(timestamp, data)]
        self.match_window = timedelta(seconds=match_window_seconds)
        self.matched_devices = []

    def add_device_source1(self, mac_address, data):
        """Přidá zařízení z prvního zdroje"""
        timestamp = datetime.now()
        self.source1_devices[mac_address].append((timestamp, data))
        self._cleanup_old_data()
        self._check_matches(mac_address)

    def add_device_source2(self, mac_address, data):
        """Přidá zařízení z druhého zdroje"""
        timestamp = datetime.now()
        self.source2_devices[mac_address].append((timestamp, data))
        self._cleanup_old_data()
        self._check_matches(mac_address)

    def _cleanup_old_data(self):
        """Vyčistí stará data mimo časové okno"""
        current_time = datetime.now()
        
        for devices in [self.source1_devices, self.source2_devices]:
            for mac in list(devices.keys()):
                devices[mac] = [
                    (ts, data) for ts, data in devices[mac]
                    if current_time - ts <= self.match_window
                ]
                if not devices[mac]:
                    del devices[mac]

    def _check_matches(self, mac_address):
        """Kontroluje, zda existuje shoda pro dané MAC adresy"""
        current_time = datetime.now()
        
        if mac_address in self.source1_devices and mac_address in self.source2_devices:
            source1_recent = self.source1_devices[mac_address][-1]
            source2_recent = self.source2_devices[mac_address][-1]
            
            if abs((source1_recent[0] - source2_recent[0]).total_seconds()) <= self.match_window.total_seconds():
                matched_data = {
                    "mac": mac_address,
                    "timestamp": current_time.timestamp(),
                    "source1_data": source1_recent[1],
                    "source2_data": source2_recent[1]
                }
                self.matched_devices.append(matched_data)
                print(f"✅ Nalezena shoda pro MAC: {mac_address}")

    def get_matched_devices(self):
        """Vrátí seznam spárovaných zařízení a vyčistí jej"""
        matches = self.matched_devices.copy()
        self.matched_devices.clear()
        return matches

# Příklad použití
async def example_usage():
    comparator = DeviceComparator(match_window_seconds=30)
    
    # Simulace dat z prvního zdroje
    comparator.add_device_source1(
        "00:11:22:33:44:55",
        {"name": "Device1", "rssi": -65}
    )
    
    # Simulace dat z druhého zdroje
    comparator.add_device_source2(
        "00:11:22:33:44:55",
        {"name": "Device1", "signal": -67}
    )
    
    # Získání spárovaných zařízení
    matched = comparator.get_matched_devices()
    for device in matched:
        print(f"Matched device: {device}")

import json
from mqttportabo import send_payload

async def process_ble_message(message, comparator):
    """
    Processes a BLE message, compares the MAC address, and sends the UUID via MQTT if matched.
    """
    mac_address = message.get("mac")
    uuid = message.get("uuid")

    if not mac_address or not uuid:
        print("❌ Invalid BLE message: Missing MAC or UUID")
        return

    # Add the device to source1 for comparison
    comparator.add_device_source1(mac_address, {"uuid": uuid})

    # Check for matches
    matched_devices = comparator.get_matched_devices()
    for device in matched_devices:
        try:
            payload = {"uuid": device["source1_data"]["uuid"]}
            send_payload("verified_devices", payload)
            print(f"📤 Sent UUID: {payload['uuid']} for MAC: {device['mac']}")
        except Exception as e:
            print(f"❌ Error sending UUID: {e}")

# Example usage with BLE message processing
async def example_usage():
    comparator = DeviceComparator(match_window_seconds=30)

    # Simulated BLE message
    ble_message = {
        "mac": "00:11:22:33:44:55",
        "uuid": "0000180f-0000-1000-8000-00805f9b34fb"
    }

    await process_ble_message(ble_message, comparator)

if __name__ == "__main__":
    asyncio.run(example_usage())