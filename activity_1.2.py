import os

# ============================================================
# Activity 1.2 - Password Generator
# UFCFYR-15-2 Advanced Algorithms Coursework
# ============================================================
# Generates ALL valid passwords of a user-specified length.
#
# Character sets (hard-coded as per the brief):
#   Capital letters  : {A, B, C, D, E}
#   Lowercase letters: {a, b, c, d, e}
#   Digits           : {1, 2, 3, 4, 5}
#   Special symbols  : {$, &, %}
#
# Password rules:
#   1. Must contain at least ONE character from EACH category
#   2. Must START with a letter (capital OR lowercase)
#   3. At most TWO capital letters
#   4. At most TWO special symbols
#
# Algorithm: Recursive Backtracking with Early Pruning
#   Instead of generating every possible combination and then
#   filtering (brute force), we BUILD passwords character by
#   character and PRUNE branches the moment they violate a rule.
#   This avoids exploring millions of dead-end combinations.
# ============================================================

OUTPUT_FILE = os.path.join("activity1_2", "passwords.txt")

# --- Character sets defined as sorted lists for consistent output order ---
CAPITALS = ['A', 'B', 'C', 'D', 'E']
LOWERS   = ['a', 'b', 'c', 'd', 'e']
DIGITS   = ['1', '2', '3', '4', '5']
SYMBOLS  = ['$', '%', '&']          # sorted alphabetically by ASCII value

# Convert to sets for O(1) membership checks inside the hot loop
CAPS_SET    = set(CAPITALS)
LOWERS_SET  = set(LOWERS)
DIGITS_SET  = set(DIGITS)
SYMBOLS_SET = set(SYMBOLS)

# Pool for position 0 (MUST start with a letter — rule 2)
LETTERS_POOL = CAPITALS + LOWERS

# Pool for all other positions (any character is allowed subject to rules)
FULL_POOL    = CAPITALS + LOWERS + DIGITS + SYMBOLS


# ============================================================
# CORE ALGORITHM: Backtracking Generator
# ============================================================

def generate_passwords(length):
    """
    Generate all valid passwords of the given length.

    This function uses RECURSIVE BACKTRACKING — a well-known algorithm
    design technique.  The key idea is:

        "Build the password one character at a time. At each step,
         only try characters that CAN still lead to a valid result.
         If the current partial password is already invalid (or can
         never become valid), stop and go back (backtrack)."

    This is much more efficient than brute force because we prune
    entire subtrees of invalid passwords without ever exploring them.

    The function is a GENERATOR (uses 'yield') — this means it produces
    one password at a time instead of building a giant list.  This keeps
    memory usage low: we write each password to the file immediately
    without storing all of them in RAM at once.

    Parameters:
        length (int) : required password length

    Yields:
        str : each valid password, one at a time
    """

    def backtrack(pos, current, n_caps, n_symbols,
                  has_cap, has_lower, has_digit, has_symbol):
        """
        Recursive helper — builds the password position by position.

        Parameters:
            pos        : index of the position we are currently filling (0-based)
            current    : list of characters chosen so far (mutable, shared)
            n_caps     : how many capital letters we have placed so far
            n_symbols  : how many special symbols we have placed so far
            has_cap    : True if at least one capital letter is in current
            has_lower  : True if at least one lowercase letter is in current
            has_digit  : True if at least one digit is in current
            has_symbol : True if at least one special symbol is in current
        """

        # ---- BASE CASE: password is fully built ----
        if pos == length:
            # Rule 1: only yield if ALL four categories are present
            if has_cap and has_lower and has_digit and has_symbol:
                yield ''.join(current)
            return  # nothing more to do at this branch

        # ---- PRUNING CHECK (Early termination) ----
        # Count how many categories have NOT yet been satisfied
        categories_still_needed = (
            (not has_cap) +      # 1 if we still need a capital letter
            (not has_lower) +    # 1 if we still need a lowercase letter
            (not has_digit) +    # 1 if we still need a digit
            (not has_symbol)     # 1 if we still need a special symbol
        )
        positions_remaining = length - pos

        if categories_still_needed > positions_remaining:
            # Even if every remaining position is a different new category,
            # we still cannot satisfy all four rules — prune this branch.
            return

        # ---- CHOOSE CHARACTER POOL ----
        # Rule 2: position 0 must be a letter (capital or lowercase)
        pool = LETTERS_POOL if pos == 0 else FULL_POOL

        # ---- TRY EACH CHARACTER IN THE POOL ----
        for char in pool:

            # --- Rule 3: at most 2 capital letters ---
            new_n_caps = n_caps + (1 if char in CAPS_SET else 0)
            if new_n_caps > 2:
                continue  # placing this capital would break rule 3 — skip it

            # --- Rule 4: at most 2 special symbols ---
            new_n_symbols = n_symbols + (1 if char in SYMBOLS_SET else 0)
            if new_n_symbols > 2:
                continue  # placing this symbol would break rule 4 — skip it

            # ---- PLACE the character and RECURSE into the next position ----
            current.append(char)

            yield from backtrack(
                pos + 1,                          # move to the next position
                current,                          # updated password so far
                new_n_caps,                       # updated capital count
                new_n_symbols,                    # updated symbol count
                has_cap    or char in CAPS_SET,   # did we just add a capital?
                has_lower  or char in LOWERS_SET, # did we just add a lowercase?
                has_digit  or char in DIGITS_SET, # did we just add a digit?
                has_symbol or char in SYMBOLS_SET # did we just add a symbol?
            )

            # ---- BACKTRACK: remove the character and try the next option ----
            # This restores 'current' so we can try a different character
            # at this same position.
            current.pop()

    # Start the recursion: position 0, empty password, all counts at zero
    yield from backtrack(
        pos=0, current=[],
        n_caps=0, n_symbols=0,
        has_cap=False, has_lower=False, has_digit=False, has_symbol=False
    )


# ============================================================
# INPUT / OUTPUT
# ============================================================

def get_password_length():
    """
    Prompt the user to enter a valid password length.

    A minimum length of 4 is enforced because:
    - Rule 1 requires at least one character from each of the 4 categories
    - Therefore the shortest possible valid password is length 4

    Returns:
        int : validated password length
    """
    while True:
        try:
            length = int(input("Enter the desired password length: "))
            if length < 4:
                print("  Minimum length is 4 "
                      "(need at least 1 from each: capitals, lowercase, digits, symbols).")
            else:
                return length
        except ValueError:
            print("  Invalid input — please enter a whole number.")


def main():
    """
    Main function:
      1. Ask user for password length
      2. Generate all valid passwords using backtracking
      3. Print each password (with index) to the console
      4. Save all passwords to a text file
    """

    # Step 1: Get length from user
    length = get_password_length()

    # Build the output path relative to this script's directory
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, OUTPUT_FILE)

    # Make sure the output folder exists (create it if necessary)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"\nGenerating all valid passwords of length {length}...")
    print("Passwords are written to file as they are generated (memory-efficient).\n")

    count = 0

    # Open the output file once and stream passwords into it
    with open(output_path, 'w', encoding='utf-8') as f:

        for password in generate_passwords(length):
            count += 1
            line = f"{count} {password}"
            print(line)            # display on screen
            f.write(line + '\n')   # write to file immediately (no buffering needed)

    # Summary
    print(f"\nTotal valid passwords generated : {count}")
    print(f"Results saved to               : {output_path}")


if __name__ == "__main__":
    main()
