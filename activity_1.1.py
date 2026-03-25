import csv
import os
from collections import Counter

# ============================================================
# Activity 1.1 - Degree Classification System
# UFCFYR-15-2 Advanced Algorithms Coursework
# ============================================================
# This program loads student module marks and module reference
# data from CSV files, then calculates each student's final
# degree classification using UWE Academic Regulations 23/24.
# Results are saved to a CSV output file.
# ============================================================

# --- FILE PATHS (relative to this script's location) ---
MODULES_FILE = os.path.join("activity1_1", "cs modules.csv")
MARKS_FILE   = os.path.join("activity1_1", "activity1_1_marks.csv")
OUTPUT_FILE  = os.path.join("activity1_1", "degree_results.csv")

# Level 5 (Year 2): only the best 100 credits count toward the average
LEVEL5_TARGET_CREDITS = 100


# ============================================================
# SECTION 1: Data Loading
# ============================================================

def parse_module_code(code):
    """
    Extract the credit value and academic level from a UWE module code.

    UWE module codes follow the pattern:  UFCFXX-CC-L
        XX = module identifier (letters/numbers)
        CC = credit value (e.g. 15 or 30)
        L  = academic level (1 = Year 1, 2 = Year 2, 3 = Year 3)

    Example: 'UFCF7S-30-2'  ->  credits=30, level=2

    Returns:
        (credits: int, level: int)
    """
    parts = code.strip().split('-')
    credits = int(parts[1])   # middle segment holds the credit value
    level   = int(parts[2])   # last segment holds the level/year
    return credits, level


def load_modules(filepath):
    """
    Load the module reference file (module codes and names).

    Expected CSV format (no header):
        module_code, module_name

    Returns:
        dict  {module_code: module_name}
    """
    modules = {}
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2 and row[0].strip():
                code = row[0].strip()
                name = row[1].strip()
                modules[code] = name
    return modules


def load_student_marks(filepath):
    """
    Load all student marks from the marks CSV file.

    Each row represents one student, formatted as:
        student_id, module_code_1, mark_1, module_code_2, mark_2, ...

    Marks are stored as floats where possible.
    Non-numeric marks (e.g. 'P', 'F' for pass/fail modules) are stored
    as strings and will be excluded from average calculations.

    Returns:
        list of dicts:  [{'id': str, 'marks': {code: mark}}, ...]
    """
    students = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0].strip():
                continue  # skip any blank rows

            student_id = row[0].strip()
            marks = {}

            # Data alternates: module_code, mark, module_code, mark, ...
            # We step through in pairs starting at index 1
            i = 1
            while i + 1 < len(row):
                code      = row[i].strip()
                mark_raw  = row[i + 1].strip()

                try:
                    marks[code] = float(mark_raw)  # numeric mark
                except ValueError:
                    marks[code] = mark_raw          # pass/fail string (P/F)

                i += 2  # advance to the next (code, mark) pair

            students.append({'id': student_id, 'marks': marks})

    return students


# ============================================================
# SECTION 2: Degree Calculation Logic
# ============================================================

def check_all_passed(marks):
    """
    Check whether a student has passed every module they took.

    UWE Regulation: a student must pass ALL modules from Years 1, 2 and 3
    to be eligible for an award.  A pass requires a mark of 40 or above.
    Pass/fail modules (non-numeric marks) are not checked here.

    Returns:
        True  - all numeric marks are >= 40
        False - at least one numeric mark is below 40
    """
    for code, mark in marks.items():
        if isinstance(mark, float) and mark < 40:
            return False  # this module was failed
    return True


def select_best_level5_modules(marks, target_credits=100):
    """
    Select the highest-scoring Level 5 (Year 2) modules up to target_credits.

    UWE Regulation: the Level 5 weighted average is computed using the BEST
    modules across 100 credits.  This rewards strong performance and means
    a student is not penalised for taking extra optional modules.

    Algorithm (greedy selection):
        1. Collect all Year 2 modules that have a numeric mark
        2. Sort them by mark (highest first)
        3. Add modules one by one until we reach target_credits or run out

    The greedy approach is correct here: because we want the highest
    weighted average, we should always prefer higher-mark modules first.

    Returns:
        list of tuples  [(module_code, credits, mark), ...]
    """
    level5_candidates = []

    for code, mark in marks.items():
        if not isinstance(mark, float):
            continue  # skip pass/fail modules (non-numeric)
        try:
            credits, level = parse_module_code(code)
        except (ValueError, IndexError):
            continue

        if level == 2:  # Level 5 = Year 2 in UWE terminology
            level5_candidates.append((code, credits, mark))

    # Sort by mark descending so we greedily pick the best ones first
    level5_candidates.sort(key=lambda x: x[2], reverse=True)

    selected      = []
    total_credits = 0

    for code, credits, mark in level5_candidates:
        # Only add if we won't exceed the 100-credit target
        if total_credits + credits <= target_credits:
            selected.append((code, credits, mark))
            total_credits += credits
            if total_credits == target_credits:
                break  # reached exactly 100 credits — stop early

    return selected


def get_level6_modules(marks):
    """
    Collect all Level 6 (Year 3) modules that have a numeric mark.

    UWE Regulation: ALL Level 6 credits count toward the weighted average
    (no selection/dropping — every Year 3 module the student sat is included).
    Pass/fail modules are excluded from the average calculation.

    Returns:
        list of tuples  [(module_code, credits, mark), ...]
    """
    level6 = []

    for code, mark in marks.items():
        if not isinstance(mark, float):
            continue  # skip pass/fail modules
        try:
            credits, level = parse_module_code(code)
        except (ValueError, IndexError):
            continue

        if level == 3:  # Level 6 = Year 3
            level6.append((code, credits, mark))

    return level6


def weighted_average(modules):
    """
    Calculate the credit-weighted average mark for a set of modules.

    Formula:
        weighted_avg = sum(credit_i * mark_i) / sum(credit_i)

    This means a 30-credit module contributes twice as much as
    a 15-credit module — reflecting the greater workload involved.

    Returns:
        float: weighted average mark, or 0.0 if no modules given
    """
    if not modules:
        return 0.0

    total_weighted = sum(credits * mark for _, credits, mark in modules)
    total_credits  = sum(credits        for _, credits, _    in modules)

    if total_credits == 0:
        return 0.0

    return total_weighted / total_credits


def get_degree_classification(aggregate):
    """
    Convert a final aggregate mark into a degree classification label.

    UWE Award Bands:
        >= 70   →  First Class
        60-69   →  Second Class (Upper Division) — 2:1
        50-59   →  Second Class (Lower Division) — 2:2
        40-49   →  Third Class
        < 40    →  Fail

    Returns:
        str: degree classification label
    """
    if aggregate >= 70:
        return "First Class"
    elif aggregate >= 60:
        return "Second Class (Upper Division) - 2:1"
    elif aggregate >= 50:
        return "Second Class (Lower Division) - 2:2"
    elif aggregate >= 40:
        return "Third Class"
    else:
        return "Fail"


def calculate_student_degree(student):
    """
    Run the full degree classification calculation for one student.

    Step-by-step process:
        1. Check every module is passed (mark >= 40).
           If any module is failed, award classification = 'Fail'.
        2. Select the best 100 Level 5 credits (greedy by mark).
           Compute Level 5 weighted average.
        3. Use all Level 6 modules to compute Level 6 weighted average.
        4. Combine in a 3:1 ratio:
               aggregate = (L6_avg * 3 + L5_avg * 1) / 4
        5. Map the aggregate to a degree band.

    Returns:
        dict with keys:
            id             - student identifier
            passed_all     - True/False
            level5_avg     - Level 5 weighted average (or None if failed)
            level6_avg     - Level 6 weighted average (or None if failed)
            aggregate      - final aggregate mark  (or None if failed)
            classification - degree band string
    """
    student_id = student['id']
    marks      = student['marks']

    # ----- Step 1: Module pass check -----
    if not check_all_passed(marks):
        # A failed module means no degree can be awarded
        return {
            'id'             : student_id,
            'passed_all'     : False,
            'level5_avg'     : None,
            'level6_avg'     : None,
            'aggregate'      : None,
            'classification' : 'Fail (failed module(s))'
        }

    # ----- Step 2: Level 5 (Year 2) — best 100 credits -----
    level5_modules = select_best_level5_modules(marks, LEVEL5_TARGET_CREDITS)
    level5_avg     = weighted_average(level5_modules)

    # ----- Step 3: Level 6 (Year 3) — all modules -----
    level6_modules = get_level6_modules(marks)
    level6_avg     = weighted_average(level6_modules)

    # ----- Step 4: Final aggregate (3:1 ratio — L6 weighted more heavily) -----
    aggregate = (level6_avg * 3 + level5_avg * 1) / 4

    # ----- Step 5: Degree band -----
    classification = get_degree_classification(aggregate)

    return {
        'id'             : student_id,
        'passed_all'     : True,
        'level5_avg'     : round(level5_avg, 2),
        'level6_avg'     : round(level6_avg, 2),
        'aggregate'      : round(aggregate,  2),
        'classification' : classification
    }


# ============================================================
# SECTION 3: Output
# ============================================================

def save_results(results, filepath):
    """
    Write all student degree results to a CSV file.

    Output columns:
        Student ID | Passed All | Level 5 Avg | Level 6 Avg |
        Final Aggregate | Degree Classification
    """
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header row
        writer.writerow([
            'Student ID',
            'Passed All Modules',
            'Level 5 Weighted Avg (%)',
            'Level 6 Weighted Avg (%)',
            'Final Aggregate Mark (%)',
            'Degree Classification'
        ])

        # One row per student
        for r in results:
            writer.writerow([
                r['id'],
                'Yes' if r['passed_all'] else 'No',
                r['level5_avg']  if r['level5_avg']  is not None else 'N/A',
                r['level6_avg']  if r['level6_avg']  is not None else 'N/A',
                r['aggregate']   if r['aggregate']   is not None else 'N/A',
                r['classification']
            ])

    print(f"\nResults saved to: {filepath}")


def print_summary(results):
    """
    Print a console summary showing how many students got each classification.
    """
    counts = Counter(r['classification'] for r in results)

    print("\n--- Degree Classification Summary ---")
    # Define a display order for the classifications
    order = [
        "First Class",
        "Second Class (Upper Division) - 2:1",
        "Second Class (Lower Division) - 2:2",
        "Third Class",
        "Fail",
        "Fail (failed module(s))"
    ]
    for band in order:
        if band in counts:
            print(f"  {band:<45} : {counts[band]} students")
    print(f"  {'TOTAL':<45} : {len(results)} students")


# ============================================================
# SECTION 4: Main Entry Point
# ============================================================

def main():
    """
    Orchestrates the degree calculation system:
        1. Resolve file paths relative to the script location
        2. Load the module reference data (names + codes)
        3. Load all student marks
        4. Calculate degree classification for every student
        5. Save results to CSV and print a summary to the console
    """
    # Build absolute paths so the script works regardless of working directory
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    modules_path = os.path.join(script_dir, MODULES_FILE)
    marks_path   = os.path.join(script_dir, MARKS_FILE)
    output_path  = os.path.join(script_dir, OUTPUT_FILE)

    # --- Load data ---
    print("Loading module reference data...")
    modules_info = load_modules(modules_path)
    print(f"  Found {len(modules_info)} modules.")

    print("Loading student marks...")
    students = load_student_marks(marks_path)
    print(f"  Found {len(students)} students.")

    # --- Process each student ---
    print("Calculating degree classifications...")
    results = [calculate_student_degree(s) for s in students]

    # --- Output ---
    save_results(results, output_path)
    print_summary(results)


if __name__ == "__main__":
    main()
