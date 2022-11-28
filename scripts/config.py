#changer config .json en python 
import json

with open("settings.json", "r") as jsonfile:
    data = json.load(jsonfile)
print(data)



