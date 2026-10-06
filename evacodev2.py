import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter

class Duration:
    SHORT = "SHORT"
    STANDARD = "STANDARD"
    LONG = "LONG"

with open("eva-data.json", "r", encoding="utf-8") as file:
    eva_data = json.load(file)


records = []

for eva in eva_data:
    date_text = eva.get("date")
    duration_text = eva.get("duration")

    if not date_text or not duration_text:
        continue

    date = datetime.fromisoformat(date_text)
    hours, minutes = map(int, duration_text.split(":"))
    duration_hours = hours + minutes / 60

    if duration_hours < 4:
        records.append((date, duration_hours, eva.get("country"), Duration.SHORT))
    elif duration_hours < 7:
        records.append((date, duration_hours, eva.get("country"), Duration.STANDARD))
    elif duration_hours >= 7:
        records.append((date, duration_hours, eva.get("country"), Duration.LONG))
    

records.sort(key=lambda record: record[0])

dates = []
total_hours = 0
cumulative_hours_total = []
country_counts = Counter()
duration_counts = Counter()

for date, duration_hours, country, duration in records:
    total_hours += duration_hours
    dates.append(date)  
    cumulative_hours_total.append(total_hours)
    country_counts[country] += duration_hours
    duration_counts[duration] += duration_hours

sorted_country_counts = dict(sorted(country_counts.items(), key=lambda x:x[1], reverse=True))
sorted_duration_counts = dict(sorted(duration_counts.items(), key=lambda x:x[1], reverse=True))


#Display the total hours for each country and duration
print('--------------------------------')
for country in sorted_country_counts:
    print(f"Total hours for {country}: {sorted_country_counts[country]} \n")
for duration in sorted_duration_counts:
    print(f"Total hours for {duration}: {sorted_duration_counts[duration]} \n")
print(f"Total hours for total: {total_hours} \n --------------------------------")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))  # 1 row, 2 columns

ax1.plot(dates, cumulative_hours_total)
ax1.set_xlabel("Year")
ax1.set_ylabel("Cumulative EVA duration (hours)")
ax1.set_title("Cumulative EVA duration")

ax2.bar(sorted_country_counts.keys(), sorted_country_counts.values())
ax2.set_xlabel("Country")
ax2.set_ylabel("Cumulative EVA duration per country (hours)(Decending Order)")
ax2.set_title("EVA duration by country")
ax2.tick_params(axis="x", rotation=45) 

fig.tight_layout()
fig.savefig("images/cumulative_duration_combined.png")
plt.show()
