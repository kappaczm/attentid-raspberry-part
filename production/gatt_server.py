import asyncio
from bleak import BleakServer

# Define the GATT service and characteristic UUIDs
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

# Callback for when data is written to the characteristic
async def write_callback(sender, data):
    print(f"Received data: {data}")
    # Here you can forward the data to prijimac.py or process it as needed

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