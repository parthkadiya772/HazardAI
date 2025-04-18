import json
import os

# File name for the dataset
FILE_NAME = "Path/to/your_dataset/*.json"

def load_existing_data(file_name):
    """Load existing data from the JSON file if it exists."""
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            return json.load(f)
    return []

def save_data(file_name, data):
    """Save data to the JSON file."""
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

def add_mitigations(data):
    """Add mitigations to hazards that lack them."""
    print("\nAdding mitigations to hazards...")

    # Transform strings into dictionaries if necessary
    for i, entry in enumerate(data):
        if isinstance(entry, str):  # If entry is a string, transform it
            data[i] = {"hazard": entry, "mitigation": ""}

    # Add mitigations to hazards
    for entry in data:
        if "mitigation" not in entry or entry.get("mitigation") == "":
            print(f"\nHazard: {entry['hazard']}")
            mitigation = input("Enter the mitigation for this hazard: ").strip()
            entry["mitigation"] = mitigation
            print("Mitigation added successfully!")



def display_dataset_stats(data):
    """Display statistics about the dataset."""
    print("\nDataset Statistics:")
    print(f"Total Hazards: {len(data)}")
    hazards_with_mitigation = sum(1 for entry in data if "mitigation" in entry and entry["mitigation"])
    print(f"Hazards with Mitigation: {hazards_with_mitigation}")
    print(f"Hazards without Mitigation: {len(data) - hazards_with_mitigation}")

def display_dataset(data):
    """Display the entire dataset."""
    print("\nCurrent Dataset:")
    for i, entry in enumerate(data, 1):
        print(f"{i}. Hazard: {entry['hazard']}")
        if "mitigation" in entry and entry["mitigation"]:
            print(f"   Mitigation: {entry['mitigation']}")
        else:
            print("   Mitigation: Not provided")

def main():
    """Main function to run the hazard dataset enrichment tool."""
    print("Hazard Dataset Enrichment Tool")
    print("-" * 50)
    
    # Load existing data
    data = load_existing_data(FILE_NAME)
    
    while True:
        print("\nOptions:")
        print("1. Display dataset")
        print("2. Add mitigations to hazards")
        print("3. Display dataset statistics")
        print("4. Save and exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            display_dataset(data)
        elif choice == '2':
            add_mitigations(data)
        elif choice == '3':
            display_dataset_stats(data)
        elif choice == '4':
            save_data(FILE_NAME, data)
            print("Dataset saved successfully! Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
