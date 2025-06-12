# Smart laddklient – Battery Management Services (Python)

Detta projekt är en inlämningsuppgift i kursen om batterihanteringstjänster vid Högskolan i Skövde.

## Syfte
Skapa en klientapplikation som:
- kommunicerar med en simulerad laddstation via JSON
- laddar batteriet från 20 % till 80 % automatiskt
- endast när elpriset är lågt och hushållets belastning är under gränsvärde

##  Teknik
- Python 3
- Flask (för servern)
- REST API via JSON
- Körs i terminal (ingen GUI krävs)

##  Funktioner
Klienten (`client.py`) hämtar data varje timme från servern:
- `/info` – batterinivå, tid och laddstatus
- `/baseload` – hushållets energiförbrukning
- `/priceperhour` – elpris per timme
- `/charge` – startar eller stoppar laddningen

### Villkor för att starta laddning:
- Pris < 50 öre/kWh
- Last < 11 kW
- Batteriet < 80 %

Klienten avslutar automatiskt när batteriet når 80 %, och skriver en laddningsrapport.

##  Starta projektet
```bash
python charging_simulation.py   # Startar servern
python client.py                # Kör klienten




README - Smart EV Charging Client (VG Level)

Detta projekt implementerar en avancerad BMS-klient för simulering av smart laddning av elbil, utformad för att uppfylla kriterierna för VG-nivå i kursen "Battery Management Services" vid Högskolan i Skövde.

##  Huvudfunktioner

*  Smart laddplanering baserad på elpris, förbrukning och bilens tillgänglighet
*  Simulerad tid med 30-minuters steg (48 steg = 24 timmar)
*  Automatisk återställning (discharge till 20%) vid varje körning
*  Dynamisk beräkning av energibehov utifrån SOC och batterikapacitet
*  Schemalägger de billigaste timmarna för laddning mellan ankomst och avgång

---

##  Förklaring av programflödet

### 1. Import av bibliotek och definition av API-endpoints

```python
import requests
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"
```

Programmet använder `requests` för att kommunicera med en lokal server via REST-API, samt `datetime` för att hämta aktuell systemtid.

---

### 2. Funktioner för API-anrop

```python
def get_info():
    return requests.get(f"{BASE_URL}/info").json()

def get_baseload():
    return requests.get(f"{BASE_URL}/baseload").json()

def get_prices():
    return requests.get(f"{BASE_URL}/priceperhour").json()

def set_charging(state):
    requests.post(f"{BASE_URL}/charge", json={"charging": "on" if state else "off"})
```

Dessa funktioner hämtar aktuell laddstatus, hushållets förbrukning, Nordpools elpriser och skickar laddkommandon till servern.

---

### 3. Discharge/reset vid varje start

```python
def reset_simulation():
    requests.post(f"{BASE_URL}/discharge", json={"discharging": "on"})
```

Detta återställer simuleringen till SOC = 20% innan en ny körning börjar.

---

### 4. Huvudfunktion: main()

```python
now = datetime.now()
arrival_hour = now.hour
departure_hour = 7
```

Startar vid aktuell tidpunkt (t.ex. 18:00) och definierar en önskad sluttid för laddning (t.ex. 07:00).

```python
battery_kwh = info['battery_capacity_kWh']
soc = (battery_kwh / Q_available) * 100
```

SOC beräknas från batterikapacitet (ex. 46.3 kWh).

```python
energy_needed = (100 - soc)/100 * Q_available
slots_needed = round(energy_needed / I_charge / 0.5)
```

Beräknar hur många 30-minuterssteg som behövs för att nå 100%.

---

### 5. Välja de billigaste tillgängliga tiderna för laddning

```python
for step in range(0, 24):
    h = (arrival_hour + step) % 24
    if car_available[h] and baseload[h] < 11:
        possible_slots.append((prices[h], h))

possible_slots.sort()
chosen_hours = [h for _, h in possible_slots[:slots_needed]]
```

Programmet analyserar alla möjliga laddningssteg inom nästa 24 timmar och väljer de billigaste.

---

### 6. Simulerad exekvering

```python
for _ in range(48):
    if hour in chosen_hours:
        set_charging(True)
    else:
        set_charging(False)
    ...
```

Programmet visar laddbeslut vid varje steg med SOC, pris, förbrukning och beslutet.

---

##  Exempel på terminalutskrift

```
 Smart Charging Plan from 18:00 to 7:00
Target SOC: 100% | Currently: 20.0%
Energy needed: 37.0 kWh (~10 steps)
Chosen hours: [2, 3, 4, 13, 15, 19, 20, 21, 22, 23]

[20:00] Charging ON (Scheduled) | SOC: 55.96% | Price: 34.29 öre | Load: 0.99 kW
...
[07:00] SOC reached 100%. Done.
```

---

##  Starta programmet

```bash
python client_smart_schedule_reset.py
```

---

##  Sammanfattning

Denna programkod demonstrerar en komplett smart laddklient med:

* energibehovsanalys
* API-integration
* prisoptimering
* simulering av laddstrategi