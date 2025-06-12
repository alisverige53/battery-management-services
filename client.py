
import requests
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def get_info():
    return requests.get(f"{BASE_URL}/info").json()

def get_baseload():
    return requests.get(f"{BASE_URL}/baseload").json()

def get_prices():
    return requests.get(f"{BASE_URL}/priceperhour").json()

def set_charging(state):
    requests.post(f"{BASE_URL}/charge", json={"charging": "on" if state else "off"})

def reset_simulation():
    try:
        requests.post(f"{BASE_URL}/discharge", json={"discharging": "on"})
        print(" Simulation reset (discharge to 20%)")
    except:
        print(" Failed to reset simulation.")

def main():
    reset_simulation()
    prices = get_prices()
    baseload = get_baseload()

    Q_available = 46.3  # battery full capacity
    I_charge = 7.4  # kW charging rate
    delta_t = 0.5  # 30 minutes step in hours

    car_available = [
        False, False, True, True, True,
        False, False, True, True, True,
        True, True, True, True, False,
        True, True, False, False, True,
        True, True, True, True
    ]

    now = datetime.now()
    arrival_hour = now.hour
    departure_hour = 7  # define end hour for full charge

    info = get_info()
    battery_kwh = info['battery_capacity_kWh']
    soc = (battery_kwh / Q_available) * 100

    soc_needed = 80 - soc
    energy_needed = (soc_needed / 100) * Q_available
    hours_needed = energy_needed / I_charge
    slots_needed = round(hours_needed / delta_t)

    possible_slots = []
    for step in range(0, 24):  # next 24 hours
        h = (arrival_hour + step) % 24
        if car_available[h] and baseload[h] < 11:
            possible_slots.append((prices[h], h))

    possible_slots.sort()
    chosen_hours = [h for _, h in possible_slots[:slots_needed]]

    print(f" Smart Charging Plan from {arrival_hour}:00 to {departure_hour}:00")
    print(f"Target SOC: 100% | Currently: {round(soc, 2)}%")
    print(f"Energy needed: {round(energy_needed, 2)} kWh (~{slots_needed} steps)")
    print("Chosen hours (best price):", sorted(chosen_hours))
    print()

    sim_hour = arrival_hour
    sim_minute = 0

    for _ in range(48):  # simulate 24h
        hour = sim_hour % 24
        time_label = f"[{hour:02d}:{sim_minute:02d}]"

        info = get_info()
        battery_kwh = info['battery_capacity_kWh']
        soc = (battery_kwh / Q_available) * 100

        price = prices[hour]
        load = baseload[hour]

        if soc >= 80:
            print(f" {time_label} SOC reached 80%. Done.")
            break

        if hour in chosen_hours:
            set_charging(True)
            print(f"{time_label} Charging ON  (Scheduled) | SOC: {round(soc, 2)}% | Price: {price} öre | Load: {load} kW")
        else:
            set_charging(False)
            print(f"{time_label} Charging OFF | SOC: {round(soc, 2)}% | Price: {price} öre | Load: {load} kW | Reason: Not in schedule")

        sim_minute += 30
        if sim_minute >= 60:
            sim_minute = 0
            sim_hour += 1
            if sim_hour == 24:
                sim_hour = 0

        time.sleep(1)

if __name__ == "__main__":
    main()
