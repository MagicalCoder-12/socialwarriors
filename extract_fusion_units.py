from get_game_config import get_game_config
import json

# Get the game configuration
config = get_game_config()

# Extract items from the config
items = config.get("items", [])

# Filter for fusion units (items with breeding_order)
fusion_items = [item for item in items if "breeding_order" in item]

# Create a list with id and name for each fusion unit
fusion_data = []
for item in fusion_items:
    fusion_data.append({
        "id": item["id"],
        "name": item["name"]
    })

# Sort by id for consistency
fusion_data.sort(key=lambda x: int(x["id"]))

# Write to JSON file
with open("templates/fusion_units.json", "w") as f:
    json.dump(fusion_data, f, indent=2)

print(f"Created fusion_units.json with {len(fusion_data)} items")