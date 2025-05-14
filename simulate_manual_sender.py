from utils import handle_incoming_message

def send_manual_message():
    """
    Simulate sending a message with a predefined MAC address.
    """
    # Predefined MAC address
    mac_address = "CE:3C:9F:B6:50:38"

    # Create the message
    message = {"mac": mac_address}
    print(f"Sending message: {message}")

    # Pass the message to handle_incoming_message
    handle_incoming_message(message)

if __name__ == "__main__":
    print("Manual message sender simulation.")
    print("Using predefined MAC address.")
    send_manual_message()
import asyncio
# Removed BleakAdvertiser import as it does not exist in the bleak library

def mac_to_32bit(mac: str) -> int:
    """
    Convert a MAC address to a 32-bit integer by hashing.
    """
    mac_bytes = bytes(int(x, 16) for x in mac.split(":"))
    return int.from_bytes(mac_bytes[:4], byteorder="big")

async def send_mac_as_32bit(mac: str):
    """
    Send a MAC address as a 32-bit message over BLE using advertising.
    """
    message = mac_to_32bit(mac)

    # Convert the 32-bit integer to bytes
    message_bytes = message.to_bytes(4, byteorder="big")

    try:
        async with BleakAdvertiser() as advertiser:
            await advertiser.start_advertising(data=message_bytes)
            print(f"Broadcasting MAC {mac} as 32-bit message: {message}")
            await asyncio.sleep(5)  # Advertise for 5 seconds
            await advertiser.stop_advertising()
    except Exception as e:
        print(f"Error broadcasting message: {e}")

if __name__ == "__main__":
    print("Manual MAC-to-32-bit message sender simulation.")
    asyncio.run(send_mac_as_32bit("64:D4:9C:F7:08:9A"))  # Example MAC address