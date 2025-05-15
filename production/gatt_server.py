import asyncio
from bleak import BleakServer

# Define the GATT service and characteristic UUIDs
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

# Callback for when data is written to the characteristic
async def write_callback(sender, data):
    import prijimac
    print(f"Received data: {data}")
    # Forward the data to prijimac's handle_message function
    device_address = "GATT_SERVER"  # Placeholder for server address
    uuid_uzivatele = int.from_bytes(data, byteorder='little')
    asyncio.create_task(prijimac.handle_message(device_address, uuid_uzivatele))

# Define the GATT server
async def run_server():
    server = BleakServer()
    await server.add_service(SERVICE_UUID, "Custom Service")
    await server.add_characteristic(
        SERVICE_UUID,
        CHARACTERISTIC_UUID,
        "Write Characteristic",
        write=True,
        on_write=write_callback,
    )
    print("GATT server is running...")
    await server.start()

# Run the server
asyncio.run(run_server())