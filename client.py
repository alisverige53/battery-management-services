import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def get_info():
    return requests.get(f"{BASE_URL}/info").json()

def get_baseload():
    return requests.get(f"{BASE_URL}/baseload").json()

def get_prices():
    return requests.get(f"{BASE_URL}/priceperhour").json()

def set_charging(state):
    requests.post(f"{BASE_URL}/charge", json={"charging": "on" if state else "off"})

def main():
    prices = get_prices()
    baseload = get_baseload()
    charging_log = []

    print("Smart charging started...\n")

    while True:
        info = get_info()
        hour = info['sim_time_hour']
        battery_kwh = info['battery_capacity_kWh']
        battery_percent = round(battery_kwh / 46.3 * 100, 2)
        current_load = baseload[hour]
        price = prices[hour]

        charging_allowed = battery_percent < 80 and current_load < 11 and price < 50

        if charging_allowed:
            set_charging(True)
            charging_log.append({
                "hour": hour,
                "price": price,
                "load": current_load,
                "battery": battery_percent
            })
            print(f"[{hour}:00] Charging ON | Price: {price} öre | Load: {current_load} kW | Battery: {battery_percent}%")
        else:
            set_charging(False)
            print(f"[{hour}:00] Charging OFF | Price: {price} öre | Load: {current_load} kW | Battery: {battery_percent}%")

        if battery_percent >= 80:
            set_charging(False)
            print("\nBattery reached 80%. Stopping...\n")
            break

        time.sleep(2)

    print("Charging report:")
    for entry in charging_log:
        print(f"Hour: {entry['hour']:02}, Price: {entry['price']} öre, Load: {entry['load']} kW, Battery: {round(entry['battery'], 2)}%")

if __name__ == "__main__":
    main()
