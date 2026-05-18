
import random
import string
import math
import os
import pyperclip


# ==========================================
# Get Positive Integer Input with Maximum Limit
# ==========================================
def get_positive_integer(message, maximum=None):
    while True:
        user_input = input(message)

        if not user_input.isdigit():
            print("Please enter a valid whole number.")
            continue

        number = int(user_input)

        if number <= 0:
            print("Please enter a number greater than 0.")
            continue

        if maximum is not None and number > maximum:
            print(f"Maximum allowed value is {maximum}.")
            continue

        return number


# ==========================================
# Ask Yes/No Question
# ==========================================
def ask_yes_no(message):
    while True:
        choice = input(message).strip().upper()

        if choice == "Y":
            return True
        elif choice == "N":
            return False
        else:
            print("Please enter Y or N.")


# ==========================================
# Exclude Similar Characters
# ==========================================
def exclude_similar_characters(characters):
    similar_chars = "0O1lI"

    filtered = ""
    for ch in characters:
        if ch not in similar_chars:
            filtered += ch

    return filtered


# ==========================================
# Select Character Types
# ==========================================
def select_character_types():
    print("\nSelect Character Types:")

    use_uppercase = ask_yes_no("Include Uppercase Letters (A-Z)? (Y/N): ")
    use_lowercase = ask_yes_no("Include Lowercase Letters (a-z)? (Y/N): ")
    use_numbers = ask_yes_no("Include Numbers (0-9)? (Y/N): ")
    use_symbols = ask_yes_no("Include Special Symbols (!@#$%)? (Y/N): ")

    characters = ""

    if use_uppercase:
        characters += string.ascii_uppercase

    if use_lowercase:
        characters += string.ascii_lowercase

    if use_numbers:
        characters += string.digits

    if use_symbols:
        characters += string.punctuation

    if characters == "":
        print("\nYou must select at least one character type.")
        return select_character_types()

    if ask_yes_no("Exclude similar characters (0, O, 1, l, I)? (Y/N): "):
        characters = exclude_similar_characters(characters)

        if characters == "":
            print("All characters were removed. Please select again.")
            return select_character_types()

    return characters


# ==========================================
# Generate Random Password
# ==========================================
def generate_password(length, characters):
    password = ""

    for _ in range(length):
        password += random.choice(characters)

    return password


# ==========================================
# Generate Pronounceable Password
# ==========================================
def generate_pronounceable_password(length):
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"

    password = ""

    for i in range(length):
        if i % 2 == 0:
            password += random.choice(consonants)
        else:
            password += random.choice(vowels)

    return password


# ==========================================
# Check Password Strength
# ==========================================
def check_strength(length):
    if length < 5:
        return "Weak"
    elif length < 8:
        return "Medium"
    else:
        return "Strong"


# ==========================================
# Calculate Password Entropy
# ==========================================
def calculate_entropy(length, pool_size):
    if pool_size <= 0:
        return 0

    entropy = length * math.log2(pool_size)
    return entropy


# ==========================================
# Copy First Password to Clipboard
# ==========================================
def copy_to_clipboard(password):
    try:
        pyperclip.copy(password)
        print("\nPassword copied to clipboard.")
    except Exception:
        print("\nCould not copy to clipboard.")


# ==========================================
# Get Custom File Name
# ==========================================
def get_file_name():
    file_name = input("Enter file name (without extension): ").strip()

    if file_name == "":
        file_name = "generated_passwords"

    return file_name + ".txt"


# ==========================================
# Clear Saved File
# ==========================================
def clear_saved_file(file_name):
    with open(file_name, "w") as file:
        pass

    print(f"{file_name} has been cleared.")


# ==========================================
# Save Passwords to File
# ==========================================
def save_passwords(passwords, file_name):
    with open(file_name, "a") as file:
        file.write("=" * 50 + "\n")

        for password in passwords:
            file.write(password + "\n")

    print(f"\nPasswords saved to {file_name}")


# ==========================================
# Generate Unique Passwords
# ==========================================
def generate_unique_passwords(count, length, characters, pronounceable):
    passwords = []
    seen = set()

    while len(passwords) < count:
        if pronounceable:
            password = generate_pronounceable_password(length)
        else:
            password = generate_password(length, characters)

        if password not in seen:
            seen.add(password)
            passwords.append(password)

    return passwords


# ==========================================
# Main Program
# ==========================================
def main():
    welcome = "Advanced Password Generator"
    print(welcome.center(70, "="))

    while True:
        # Password length (maximum 10)
        length = get_positive_integer(
            "\nEnter password length (1-10): ",
            10
        )

        # Number of passwords (maximum 15)
        count = get_positive_integer(
            "How many passwords do you want to generate? (1-15): ",
            15
        )

        # Pronounceable mode
        pronounceable = ask_yes_no(
            "Use pronounceable password mode? (Y/N): "
        )

        # Character selection (not needed for pronounceable mode)
        if pronounceable:
            characters = string.ascii_lowercase
        else:
            characters = select_character_types()

        # Generate unique passwords
        passwords = generate_unique_passwords(
            count,
            length,
            characters,
            pronounceable
        )

        # Display passwords
        print("\nGenerated Passwords:")
        print("-" * 60)

        pool_size = len(characters)
        entropy = calculate_entropy(length, pool_size)
        strength = check_strength(length)

        for i, password in enumerate(passwords, start=1):
            print(f"{i}. {password}")
            print(f"   Strength: {strength}")
            print(f"   Entropy : {entropy:.2f} bits")

        print("-" * 60)

        # Copy first password to clipboard
        if ask_yes_no("\nCopy first password to clipboard? (Y/N): "):
            copy_to_clipboard(passwords[0])

        # Save passwords
        if ask_yes_no("Save passwords to file? (Y/N): "):
            file_name = get_file_name()

            # Clear file if it already exists
            if os.path.exists(file_name):
                if ask_yes_no("File already exists. Clear file first? (Y/N): "):
                    clear_saved_file(file_name)

            save_passwords(passwords, file_name)

        # Play again
        if not ask_yes_no("\nGenerate more passwords? (Y/N): "):
            print("\nThank You for Using Password Generator!")
            print("Keep Coding and Keep Learning Python!\n")
            break


# ==========================================
# Run Program
# ==========================================
if __name__ == "__main__":
    main()
