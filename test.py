import requests
import random

BASE_URL = "https://tarotapi.dev/api/v1"

def get_all_tarot_cards():
    url = f"{BASE_URL}/cards"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("cards", [])
    else:
        raise Exception("Failed to fetch tarot cards.")

def get_card_details(card_short_name):
    url = f"{BASE_URL}/cards/{card_short_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Card '{card_short_name}' not found."}

if __name__ == "__main__":
    all_cards = get_all_tarot_cards()
    random.shuffle(all_cards)

    # Create a list of numbers from 1 to 78 and shuffle those
    shuffled_numbers = list(range(1, len(all_cards) + 1))
    random.shuffle(shuffled_numbers)

    print("\n🎴 Tarot Deck Shuffled 🎴")
    print("Pick 3 numbers from the shuffled list below to draw your cards.\n")

    for i, num in enumerate(shuffled_numbers):
        print(f"{num}", end="  ")
        if (i + 1) % 10 == 0:
            print()
    print("\n")

    selected_indexes = []
    for i in range(3):
        while True:
            try:
                num = int(input(f"Choose number for Card {i + 1}: "))
                if num in shuffled_numbers:
                    # Find the index of that number in shuffled_numbers, which corresponds to card index
                    idx = shuffled_numbers.index(num)
                    selected_indexes.append(idx)
                    break
                else:
                    print("Number not in the list. Please pick from the displayed numbers.")
            except ValueError:
                print("Please enter a valid integer.")

    reading = []
    for idx in selected_indexes:
        card = all_cards[idx]
        card_id = card["name_short"]
        details = get_card_details(card_id)
        print(f"Details response for card_id={card_id}:", details)  # debug print

        if "error" in details:
            reading.append({
                "card": card["name"],
                "upright": "N/A",
                "reversed": "N/A",
                "image": "N/A"
            })
        else:
            # Defensive get with fallback
            card_name = details.get("name", card["name"])
            upright = details.get("meaning_up", "N/A")
            reversed_ = details.get("meaning_rev", "N/A")
            image = details.get("image", {}).get("png", "N/A")

            reading.append({
                "card": card_name,
                "upright": upright,
                "reversed": reversed_,
                "image": image
            })


    print("\n🔮 Your Tarot Reading 🔮")
    for i, card in enumerate(reading):
        print(f"\nCard {i + 1}: {card['card']}")
        print(f"  Upright Meaning: {card['upright']}")
        print(f"  Reversed Meaning: {card['reversed']}")
        print(f"  Image URL: {card['image']}")
