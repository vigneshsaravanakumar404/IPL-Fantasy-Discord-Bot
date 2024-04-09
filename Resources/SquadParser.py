import csv
import json

# Read the CSV file
with open("Resources\Squad.csv", "r") as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Convert the data into the desired JSON format
output = []
current_owner = None
current_squad = []

for row in data:
    try:
        owner = row["OWNER"]
        status = row["STATUS"]
    except KeyError:
        print("ERROR: 'OWNER' or 'STATUS' column not found in the CSV file.")
        print("Row:", row)
        continue

    if owner != current_owner:
        if current_owner:
            output.append({"Owner": current_owner, "Squad": current_squad})
        current_owner = owner
        current_squad = []

    position = ""
    if status == "C":
        position = "C"
    elif status == "VC":
        position = "VC"

    player = {
        "old_name": row["NAME"],
        "new_name": row["NAME"],
        "isBowler": row["ISBOWLER"].lower() == "true",
        "isBatsman": row["ISBATSMAN"].lower() == "true",
        "Team": owner,
        "Position": position,
        "MOM": int(row["MOM"]),
        "6+": int(row["6+"]),
        "HT": int(row["HT"]),
    }
    current_squad.append(player)

# Append the last owner's squad
if current_owner:
    output.append({"Owner": current_owner, "Squad": current_squad})

# Convert the output to JSON and print
output_json = json.dumps(output, indent=2)
output_file = "backend\Data.json"
with open(output_file, "w") as file:
    file.write(output_json)
