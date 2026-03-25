# Advanced Algorithms Coursework Plan
**Module:** UFCFYR-15-2 Advanced Algorithms
**Deadline:** 2nd April 2026, 14:00
**Weighting:** 50% of total module mark

---

## Activity 1.1 – Degree Calculation (20%)

**Data understanding:**
- Module codes encode credits and level: `UFCFHS-30-1` → 30 credits, Level 4 (year 1), `UFCF7S-30-2` → 30 credits, Level 5 (year 2)
- Marks CSV: `student_id, mod_code, mark, mod_code, mark, ...`

**Algorithm:**
1. Parse both CSVs into dictionaries: `{mod_code: (name, credits, level)}`
2. For each student, split modules into Level 4 / 5 / 6 groups
3. **Pass check:** all modules must have mark >= 40 (fail = no degree)
4. **Level 5 weighted avg:** sort L5 modules by mark (desc), greedily pick best until exactly 100 credits — `weighted_avg_L5 = sum(credits x mark) / 100`
5. **Level 6 weighted avg:** use all L6 modules — `weighted_avg_L6 = sum(credits x mark) / total_L6_credits`
6. **Final mark:** `(weighted_avg_L6 x 3 + weighted_avg_L5 x 1) / 4`
7. Classify: >=70 First, >=60 2:1, >=50 2:2, >=40 Third, else Fail
8. Save results to CSV/text file

**Key design choice:** greedy selection for best 100 credits (sort by mark desc) is O(n log n) and optimal since we want to maximise weighted average

---

## Activity 1.2 – Password Generator (25%)

**Character sets:**
- Capitals: {A, B, C, D, E}
- Lowercase: {a, b, c, d, e}
- Digits: {1, 2, 3, 4, 5}
- Specials: {$, &, %}

**Algorithm (own implementation — no itertools for core logic):**
1. Use recursive backtracking / constraint-aware generation
2. Track counts: `n_upper`, `n_special`, position, current password chars
3. At each position, try each valid character respecting constraints:
   - Position 0: must be a letter (upper or lower)
   - `n_upper <= 2` at all times
   - `n_special <= 2` at all times
4. At the end (length reached): check that all 4 categories are represented
5. Write passwords to file with index

**Why backtracking:** prunes invalid branches early (e.g. won't try adding a 3rd capital), much more efficient than generating all permutations then filtering

---

## Activity 1.3 – Route Plan (20%)

**Algorithm: Held-Karp DP (optimal TSP)**
1. Read railway CSV into an adjacency list / weighted graph
2. For a query (list of stations to visit + start + end), extract the subgraph of those stations
3. Run **Dijkstra** between every pair of required stations to get shortest path costs (since stations may not be directly connected)
4. Run **Held-Karp** on the distance matrix of required stations:
   - `dp[visited_set][current] = min cost to reach current having visited set`
   - Reconstruct path from the DP table
5. Output total cost and full route (expanding inter-station paths)

**Why Held-Karp:** O(2^n x n^2) — optimal for small n (number of required stations), much better than brute-force O(n!)

---

## Activity 1.4 – Parallel Face Recognition (25%)

**Algorithm: multiprocessing with early termination**
1. Load known face encoding in the main process (once)
2. Determine CPU count: `os.cpu_count()`
3. Split image list into chunks — one chunk per worker
4. Use `multiprocessing.Pool` with `Pool.imap_unordered` + terminate on first match
5. Each worker processes its chunk, returns filename if match found or `None`
6. Main process collects results, prints match + time, terminates pool early

**Why `multiprocessing` not `threading`:** Python's GIL prevents true parallelism with threads; `multiprocessing` gives each worker its own interpreter — true CPU parallelism

---

## Order of Implementation

| Priority | Activity | Reason |
|----------|----------|--------|
| 1st | 1.1 | Straightforward, builds confidence |
| 2nd | 1.2 | Self-contained, no external dependencies |
| 3rd | 1.3 | More complex (graph algorithms) |
| 4th | 1.4 | Needs `face_recognition` installed |

---

## Deliverables Checklist

- [ ] `activity_1.1.py` — Degree calculation
- [ ] `activity_1.2.py` — Password generator
- [ ] `activity_1.3.py` — Route planner
- [ ] `activity_1.4.py` — Parallel face recognition
- [ ] `readme.txt` — Install instructions for non-standard libraries
- [ ] Mini report (Word/PDF) — Activity 2.1 (max 800 words)
- [ ] Short video demo — Activity 2.2 (max 8 minutes)
- [ ] Zip as `AACoursework_Your Name_Student Number.zip`
