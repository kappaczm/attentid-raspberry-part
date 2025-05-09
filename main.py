from mqttportabo import send_payload

# Logika skenovani a komunikace s Ivanovo aplikací

# Priklad pouziti a odeslani
id_uzivatele = 123
mac_adresa_uzivatele = "AB:CD:EF:12:34:56"

tohle_se_odesle = {
    "id": id_uzivatele,
    "mac": mac_adresa_uzivatele,
    "timestamp": 1691234567,  # Příklad timestampu
    "data": {
        "name": "MyBLEDevice",
        "rssi": -65,
        "uuids": ["12345678-1234-5678-1234-567812345678"],
        "manufacturer_data": {
            "76": "12020000"
        }
    }
}

send_payload("test_topic", tohle_se_odesle)
# Vypisovani dat do konzole
print("📤 Data odeslána:", tohle_se_odesle)