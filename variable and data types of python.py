import random
import string
import argparse


def generate_password(
    length: int = 12,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    exclude_chars: str = ""
) -> str:
    """
    Generate a secure random password.

    Args:
        length: Length of the password (default: 12)
        use_uppercase: Include uppercase letters (A-Z)
        use_lowercase: Include lowercase letters (a-z)
        use_digits: Include digits (0-9)
        use_symbols: Include symbols (!@#$%^&*...)
        exclude_chars: Characters to exclude from the password

    Returns:
        A randomly generated password string
    """
    if length < 4:
        raise ValueError("Password length must be at least 4.")

    character_pool = ""
    required_chars = []

    if use_uppercase:
        chars = ''.join(c for c in string.ascii_uppercase if c not in exclude_chars)
        character_pool += chars
        required_chars.append(random.choice(chars))

    if use_lowercase:
        chars = ''.join(c for c in string.ascii_lowercase if c not in exclude_chars)
        character_pool += chars
        required_chars.append(random.choice(chars))

    if use_digits:
        chars = ''.join(c for c in string.digits if c not in exclude_chars)
        character_pool += chars
        required_chars.append(random.choice(chars))

    if use_symbols:
        chars = ''.join(c for c in string.punctuation if c not in exclude_chars)
        character_pool += chars
        required_chars.append(random.choice(chars))

    if not character_pool:
        raise ValueError("At least one character type must be selected.")

    # Fill remaining length with random characters from the pool
    remaining_length = length - len(required_chars)
    remaining_chars = [random.choice(character_pool) for _ in range(remaining_length)]

    # Combine and shuffle to avoid predictable positions
    password_list = required_chars + remaining_chars
    random.shuffle(password_list)

    return ''.join(password_list)


def check_strength(password: str) -> str:
    """
    Evaluate the strength of a given password.

    Returns: 'Weak', 'Moderate', 'Strong', or 'Very Strong'
    """
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 14:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score == 3:
        return "Moderate"
    elif score == 4:
        return "Strong"
    else:
        return "Very Strong"


def generate_multiple(count: int, **kwargs) -> list[str]:
    """Generate multiple passwords at once."""
    return [generate_password(**kwargs) for _ in range(count)]


def interactive_mode():
    """Run the password generator in interactive mode."""
    print("=" * 40)
    print("       🔐 Password Generator")
    print("=" * 40)

    try:
        length = int(input("Password length (default 12): ").strip() or 12)
        count = int(input("How many passwords? (default 1): ").strip() or 1)
        use_uppercase = input("Include uppercase? (Y/n): ").strip().lower() != 'n'
        use_lowercase = input("Include lowercase? (Y/n): ").strip().lower() != 'n'
        use_digits = input("Include digits? (Y/n): ").strip().lower() != 'n'
        use_symbols = input("Include symbols? (Y/n): ").strip().lower() != 'n'
        exclude_chars = input("Characters to exclude (leave blank for none): ").strip()

        print("\n" + "-" * 40)
        passwords = generate_multiple(
            count,
            length=length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_digits=use_digits,
            use_symbols=use_symbols,
            exclude_chars=exclude_chars
        )

        for i, pwd in enumerate(passwords, 1):
            strength = check_strength(pwd)
            print(f"[{i}] {pwd}  →  Strength: {strength}")

        print("-" * 40)

    except ValueError as e:
        print(f"Error: {e}")


def cli_mode():
    """Run the password generator via command-line arguments."""
    parser = argparse.ArgumentParser(description="🔐 Python Password Generator")
    parser.add_argument("-l", "--length", type=int, default=12, help="Password length (default: 12)")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of passwords (default: 1)")
    parser.add_argument("--no-upper", action="store_false", dest="uppercase", help="Exclude uppercase letters")
    parser.add_argument("--no-lower", action="store_false", dest="lowercase", help="Exclude lowercase letters")
    parser.add_argument("--no-digits", action="store_false", dest="digits", help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_false", dest="symbols", help="Exclude symbols")
    parser.add_argument("--exclude", type=str, default="", help="Characters to exclude (e.g. 'O0lI')")
    args = parser.parse_args()

    try:
        passwords = generate_multiple(
            args.count,
            length=args.length,
            use_uppercase=args.uppercase,
            use_lowercase=args.lowercase,
            use_digits=args.digits,
            use_symbols=args.symbols,
            exclude_chars=args.exclude
        )
        for i, pwd in enumerate(passwords, 1):
            strength = check_strength(pwd)
            print(f"[{i}] {pwd}  →  Strength: {strength}")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cli_mode()
    else:
        interactive_mode()
