symptoms = set()

rules = [
    ({"powdery_patches"}, "nothing_serious"),
    ({"brown_spots"}, "nothing_serious"),
    ({"yellow_rings"}, "nothing_serious"),
    ({"soft_tissues"}, "nothing_serious"),

    ({"powdery_patches", "brown_spots"}, "fungus"),
    ({"yellow_rings", "soft_tissues"}, "bacterial"),

    ({"fungus"}, "use_protectants"),
    ({"bacterial"}, "use_bactericides")
]

treatments = {
    "fungus": "use_protectants",
    "bacterial": "use_bactericides"
}

symptom_options = {
    "1": "powdery_patches",
    "2": "brown_spots",
    "3": "yellow_rings",
    "4": "soft_tissues"
}


def display_symptoms():
    print("\n---------- CURRENT SYMPTOMS ----------")

    if not symptoms:
        print("No symptoms entered.")
        return

    for symptom in symptoms:
        print("-", symptom.replace("_", " ").title())


def select_symptom():
    print("\n---------- ENTER SYMPTOM ----------")
    print("1. Powdery Patches")
    print("2. Brown Spots")
    print("3. Yellow Rings")
    print("4. Soft Tissues")

    choice = input("Enter your choice: ")

    if choice in symptom_options:
        selected = symptom_options[choice]
        symptoms.add(selected)
        print(selected.replace("_", " ").title(), "added.")
    else:
        print("Invalid choice.")


def symptom_manager():

    while True:

        print("\n===================================")
        print("          SYMPTOM MENU")
        print("===================================")
        print("1. Add symptom")
        print("2. Show symptoms")
        print("3. Clear symptoms")
        print("4. Continue")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            select_symptom()

        elif choice == "2":
            display_symptoms()

        elif choice == "3":
            symptoms.clear()
            print("All symptoms have been cleared.")

        elif choice == "4":

            if symptoms:
                return "continue"

            print("Please enter at least one symptom.")

        elif choice == "5":
            return "exit"

        else:
            print("Invalid choice.")


def forward_chaining():

    print("\n========== FORWARD CHAINING ==========")

    known_facts = set(symptoms)

    print("Initial Facts:", known_facts)

    changed = True

    while changed:

        changed = False

        for conditions, result in rules:

            if conditions.issubset(known_facts):
                if result not in known_facts:

                    known_facts.add(result)
                    changed = True

    print("\n========== DERIVED FACTS ==========")

    for fact in known_facts:
        print("-", fact)

    print("\n========== CONCLUSION ==========")

    if "fungus" in known_facts and "bacterial" in known_facts:

        print("The plant has BOTH fungal and bacterial infection.")

        print("\nTreatment:")
        print("- Use fungal protectants.")
        print("- Use bactericides.")

    elif "fungus" in known_facts:

        print("The plant has a FUNGAL infection.")

        print("\nTreatment:")
        print("- Use fungal protectants.")

    elif "bacterial" in known_facts:

        print("The plant has a BACTERIAL infection.")

        print("\nTreatment:")
        print("- Use bactericides.")

    elif "nothing_serious" in known_facts:

        print("Cannot recognize the disease.")
        print("Your plant is getting infected.")
        print("Take care of your plant.")

    else:

        print("Disease cannot be determined")
        print("from the given symptoms.")


def backward_prove(goal, checked=None):

    if checked is None:
        checked = set()

    # Goal is already one of the entered facts
    if goal in symptoms:
        return True

    # Avoid checking the same goal repeatedly
    if goal in checked:
        return False

    checked.add(goal)

    # Search all rules that can produce the goal
    for conditions, conclusion in rules:

        if conclusion == goal:

            possible = True

            for condition in conditions:

                if not backward_prove(condition, checked):
                    possible = False
                    break

            if possible:
                return True

    return False


def backward_chaining():

    print("\n========== BACKWARD CHAINING ==========")
    print("\nWhat do you want to prove?")

    print("1. Fungus")
    print("2. Bacterial")
    print("3. Use Protectants")
    print("4. Use Bactericides")
    print("5. Nothing Serious")

    choice = input("\nEnter your choice: ")

    goal_list = {
        "1": "fungus",
        "2": "bacterial",
        "3": "use_protectants",
        "4": "use_bactericides",
        "5": "nothing_serious"
    }

    if choice not in goal_list:

        print("\nInvalid goal.")
        return

    goal = goal_list[choice]

    print("\nGoal:", goal)

    result = backward_prove(goal)

    print("\n========== RESULT ==========")

    if result:

        print("Goal PROVED:", goal)

        if goal == "fungus":

            print("\nConclusion: Fungal infection detected.")
            print("Reason: Powdery patches AND brown spots are present.")

        elif goal == "bacterial":

            print("\nConclusion: Bacterial infection detected.")
            print("Reason: Yellow rings AND soft tissues are present.")

        elif goal == "use_protectants":

            print("\nRecommendation: Use fungal protectants.")

        elif goal == "use_bactericides":

            print("\nRecommendation: Use bactericides.")

        elif goal == "nothing_serious":

            print("\nThe symptoms match the")
            print("'nothing serious' rule.")

    else:

        print("Goal NOT PROVED:", goal)

        if goal == "fungus":
            print("\nFungal infection cannot be proved.")

        elif goal == "bacterial":
            print("\nBacterial infection cannot be proved.")

        elif goal == "use_protectants":
            print("\nCannot recommend protectants.")
            print("Fungal infection could not be proved.")

        elif goal == "use_bactericides":
            print("\nCannot recommend bactericides.")
            print("Bacterial infection could not be proved.")

        elif goal == "nothing_serious":
            print("\nThe required symptom could not be established.")


def operation_menu():

    while True:

        print("\n===================================")
        print("         OPERATION MENU")
        print("===================================")

        print("1. Forward Chaining")
        print("2. Backward Chaining")
        print("3. Re-enter Symptoms")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            forward_chaining()

        elif choice == "2":

            backward_chaining()

        elif choice == "3":

            return "reenter"

        elif choice == "4":

            return "exit"

        else:

            print("Invalid choice. Try again.")


# ---------------- MAIN PROGRAM ----------------

while True:

    print("\n===================================")
    print("      PLANT DISEASE EXPERT SYSTEM")
    print("===================================")

    symptoms.clear()

    status = symptom_manager()

    if status == "exit":

        print("\nProgram ended.")
        break

    while True:

        operation = operation_menu()

        if operation == "reenter":
            break

        if operation == "exit":

            print("\nProgram ended.")
            quit()