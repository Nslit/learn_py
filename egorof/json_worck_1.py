import json

with open('manager_sales.json', 'r') as file:
    data = json.load(file)
max_total = 0
name_manager = ''
for i in data:

    total = 0
    for j in i["cars"]:
        total += j["price"]
    if total > max_total:
        max_total = total
        name_manager = f'{i["manager"]["first_name"]} {i["manager"]["last_name"]}'

print(f'{name_manager} {max_total}')