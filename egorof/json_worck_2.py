import json

with open('group_people.json', 'r') as file:
    data = json.load(file)
total = 0
id = 0

for i in data:
    counter = 0

    for j in i['people']:
        if j['gender'] == 'Female' and j['year'] > 1977:
            counter += 1
    if counter > total:
        total = counter
        id = i['id_group']

print(f'{id} {total}')