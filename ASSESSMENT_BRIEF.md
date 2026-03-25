# UFCFYR-15-2 Advanced Algorithms — Assessment Brief
**Academic Year:** 2025/26

## Submission Details
- **Deadline:** Before 14:00 on 2nd April 2026 (eligible for 48-hour late window)
- **Feedback due:** 25th May 2026
- **Type:** Individual Coursework with video demo
- **Weighting:** 50% of total module mark

---

## Activity 1 (90%)

### Activity 1.1 — Degree Calculation (20%)

Develop a final degree classification system based on UWE Academic Regulations 23/24.

**Degree bands:**
- First Class: 70%+
- 2:1: 60% to <70%
- 2:2: 50% to <60%
- Third Class: 40% to <50%
- Fail: <40%

Student must pass all modules from years 1, 2, and 3.

**Calculation steps:**
1. **Level 5 (Year 2):** Select best marks across 100 credits. Weighted average = sum(credit × mark) / total credits. Pass/fail modules excluded.
2. **Level 6 (Year 3):** Weighted average = sum(credit × mark) / total credits. Pass/fail modules excluded.
3. **Final aggregate:** (Level6 × 3 + Level5) / 4  (3:1 ratio)

**Input:** Two CSV files — module names/codes, and 300 students' marks for three years.
**Output:** Calculated degree marks and bands saved to a file.

---

### Activity 1.2 — Password Generator (25%)

Generate all valid passwords of a given length (read from console) using brute force.

**Character sets (hard-coded or read in):**
- Capital letters: {A, B, C, D, E}
- Lowercase letters: {a, b, c, d, e}
- Digits: {1, 2, 3, 4, 5}
- Special symbols: {$, &, %}

**Rules:**
- Must include at least one from each category
- Must start with a letter (capital or lowercase)
- Must not include more than two capital letters
- Must not include more than two special symbols

**Output:** All valid passwords with indices saved to a file.

Example (length 4):
```
1 Aa1$
2 Ba1$
3 Ca1$
...
```

---

### Activity 1.3 — Route Plan (20%)

Develop a route planning system for a railway logistics company.

- Each destination can be visited **once** (except start/end can be the same)
- Find the **lowest cost route** visiting all required stations
- Input: `railway_network.csv` — direct connections with weights e.g. `(Bristol Temple Meads, Bristol Parkway, 10)`
- London stations are merged into one node called `'London'`
- **Output:** Route with station names and total cost, saved to a file

---

### Activity 1.4 — Parallel Programming (25%)

Parallelise the provided serial face recognition program (`activity1_4_serial.py`).

- Uses `face_recognition` library to find one matching image in the `imageset` folder
- Modify into a program with **TRUE parallelism**
- Key concerns: **efficiency** and **memory space**

---

## Activity 2 (10%)

### Activity 2.1 — Mini Report (5%)
- Explain design choices for activities 1.1–1.4 (data structures, algorithms, justification)
- Use pseudocode or diagrams where helpful
- Focus on key algorithms only (skip well-known ones like merge sort)
- Mention any unoriginal work / libraries used
- **Under 800 words** (excluding pseudocode/diagrams)

### Activity 2.2 — Video Demo (5%)
- Under **8 minutes**
- Demonstrate all activities in order with verbal narration
- Highlight outstanding design decisions

---

## Deliverables

Submit as a single ZIP: `AACoursework_Your Name_Student Number.zip`

Must contain:
- `activity1_1.py`, `activity1_2.py`, `activity1_3.py`, `activity1_4.py`
- `readme.txt` if non-standard libraries are used
- Word/PDF report for Activity 2.1
- Video for Activity 2.2

---

## Marking Criteria Summary

| Activity | 40-49 | 50-59 | 60-69 | 70-84 | 85-100 |
|----------|-------|-------|-------|-------|--------|
| **1.1 (20%)** | Data imported, mostly correct output | Correct but inefficient | Correct & efficient, poor presentation | Well commented, reads different data | Very professional, easy to modify rules |
| **1.2 (25%)** | Library used, fails some rules | Library used, all rules met, not efficient | Library used efficiently OR own algorithm | Own algorithm, efficient | Own algorithm, superb efficiency |
| **1.3 (20%)** | Data stored well, algorithm correct but output not always correct | Correct output, route not provided | Elegant & professional, satisfies requirements | Extra features (fast input, data modification) | Beyond requirement (e.g. similarity search) |
| **1.4 (25%)** | True parallelism attempted but serial output | True parallelism, correct, not efficient | True parallelism, correct, decent efficiency | True parallelism, high efficiency per process | Beyond requirement (distributed/message passing) |
| **2.1 (5%)** | Covers ~60% of Act 1 | Covers ~80% of Act 1 | Covers all Act 1 | Excellent & profound, covers all | Fully evidenced with references |
| **2.2 (5%)** | Covers ~60% of Act 1 | Covers ~80% of Act 1 | Covers all Act 1 | Clear, algorithms explained, features emphasised | Professional presentation |

> Note: marking bands are **incremental** — higher bands require all lower band criteria.
