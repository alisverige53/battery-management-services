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
