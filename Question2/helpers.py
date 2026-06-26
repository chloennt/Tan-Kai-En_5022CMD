#algorithms, sample data, input & comparison helpers
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime
from transaction import Transaction

# ======================================================
# SAMPLE DATA
# ======================================================
def generate_sample_data(count=15):
    customers = ["Alice", "Bryan", "Carmen", "Desmond", "Elaine", "Farid"]
    products = ["Laptop", "Phone", "Headset", "Keyboard", "Monitor", "Mouse"]
    used_ids = set()
    data = []
    for _ in range(count):
        #unique random transaction ID
        while True:
            tid = random.randint(1000, 9999)
            if tid not in used_ids:
                used_ids.add(tid)
                break
        name = random.choice(customers)
        product = random.choice(products)
        amount = round(random.uniform(50, 3000), 2)
        date = f"2026-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        data.append(Transaction(tid, name, product, amount, date))
    return data

# ======================================================
# INPUT HELPERS (0 TO CANCEL)
# ======================================================
def ask_text(prompt):
    while True:
        val = input(prompt).strip()
        if val == "0":
            return None
        if val:
            return val
        print("\nThis field cannot be empty.")

def ask_number(prompt, is_int=False, max_val=None):
    while True:
        val = input(prompt).strip()
        if val == "0":
            return None
        try:
            num = int(val) if is_int else float(val)
        except ValueError:
            print("\nPlease enter a valid number.")
            continue
        if num < 0:
            print("\nValue cannot be negative.")
            continue
        if max_val is not None and num > max_val:
            print(f"\nValue cannot exceed {max_val}.")
            continue
        return num

def ask_date(prompt):
    #keep asking until a valid date, or 0 to cancel
    while True:
        val = input(prompt).strip()
        if val == "0":
            return None
        #accept single OR double digit month/day, e.g. 2025-11-5 or 2025-11-05
        parts = val.split("-")
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            try:
                #build a real date object, then re-format to clean YYYY-MM-DD
                y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
                clean = datetime(y, m, d).strftime("%Y-%m-%d")
                return clean #stored as e.g. "2025-11-05"
            except ValueError:
                pass #invalid date like month 13 falls through to error below
        print("\nInvalid date. Use format YYYY-MM-DD (e.g. 2025-11-05).")

# ======================================================
# RECURSIVE CALL COUNTER (ADVANCED FEATURE)
# ======================================================
merge_call_count = 0

def reset_call_count():
    global merge_call_count
    merge_call_count = 0

# ======================================================
# CORE ALGORITHMS (DIVIDE & CONQUER)
# ======================================================

# ---------------- Merge Sort ----------------
def merge_sort(arr, key="transaction_id"):
    #DIVIDE: count this recursive call, then split the list in half
    global merge_call_count
    merge_call_count += 1

    if len(arr) <= 1: #base case: a single item is already sorted
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)  #CONQUER: sort left half
    right = merge_sort(arr[mid:], key) #CONQUER: sort right half
    return merge(left, right, key)     #COMBINE: merge the two sorted halves

def merge(left, right, key):
    #COMBINE step: merge two sorted lists into one sorted list
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        #compare the chosen attribute (transaction_id / amount / date)
        if getattr(left[i], key) <= getattr(right[j], key):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    #add whatever is left over from either side
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# ---------------- Binary Search ----------------
def binary_search(arr, target_id):
    #arr must be sorted by transaction_id first
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2          #DIVIDE: check the middle
        if arr[mid].transaction_id == target_id:
            return arr[mid]              #found
        elif arr[mid].transaction_id < target_id:
            low = mid + 1                #CONQUER: search right half
        else:
            high = mid - 1               #CONQUER: search left half
    return None                          #not found

# ---------------- Linear Search ----------------
def linear_search(arr, target_id):
    #scans every item one by one - O(n)
    for t in arr:
        if t.transaction_id == target_id:
            return t
    return None

# ======================================================
# PERFORMANCE COMPARISONS (TABLE + GRAPH)
# ======================================================

# ---------------- Binary Search vs Linear Search ----------------
def compare_search_graph(data):
    #pad data up to 1000 records so the O(n) vs O(log n) curves are visible
    extra = list(data)
    used = set(t.transaction_id for t in extra)
    while len(extra) < 1000:
        tid = random.randint(10000, 999999)
        if tid in used:
            continue
        used.add(tid)
        extra.append(Transaction(tid, "Sample", "Item", 9.99, "2026-01-01"))

    data_sizes = [10, 50, 100, 200, 500, 1000]
    bin_times, lin_times = [], []

    print(f"{'Data Size':<12}{'Binary (µs)':<18}{'Linear (µs)':<15}")
    print("-" * 45)

    for n in data_sizes:
        subset = merge_sort(extra[:n], key="transaction_id") #binary needs sorted
        target = subset[-1].transaction_id #worst case for linear

        start = time.perf_counter()
        for _ in range(5000):
            binary_search(subset, target)
        bin_avg = (time.perf_counter() - start) / 5000 * 1e6

        start = time.perf_counter()
        for _ in range(5000):
            linear_search(subset, target)
        lin_avg = (time.perf_counter() - start) / 5000 * 1e6

        bin_times.append(bin_avg)
        lin_times.append(lin_avg)
        print(f"{n:<12}{bin_avg:<18.4f}{lin_avg:<15.4f}")
    print("-" * 45)

    plt.figure(figsize=(8, 5))
    plt.plot(data_sizes, bin_times, marker="o", label="Binary Search O(log n)")
    plt.plot(data_sizes, lin_times, marker="o", label="Linear Search O(n)")
    plt.title("Binary Search vs Linear Search")
    plt.xlabel("Number of Records")
    plt.ylabel("Average Search Time (µs)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("q2_search_performance.png", dpi=300)
    plt.show()

# ---------------- Merge Sort vs Binary Search ----------------
def compare_sort_vs_search(data):
    #pad data up to 1000 records so the curves are visible
    extra = list(data)
    used = set(t.transaction_id for t in extra)
    while len(extra) < 1000:
        tid = random.randint(10000, 999999)
        if tid in used:
            continue
        used.add(tid)
        extra.append(Transaction(tid, "Sample", "Item", 9.99, "2026-01-01"))

    data_sizes = [10, 50, 100, 200, 500, 1000]
    sort_times, search_times = [], []

    print(f"{'Data Size':<12}{'Merge Sort (µs)':<20}{'Binary Search (µs)':<18}")
    print("-" * 50)

    for n in data_sizes:
        subset = extra[:n]
        sorted_sub = merge_sort(subset, key="transaction_id")
        target = sorted_sub[-1].transaction_id

        #time Merge Sort (100 runs - sorting is heavier)
        start = time.perf_counter()
        for _ in range(100):
            merge_sort(subset, key="transaction_id")
        sort_avg = (time.perf_counter() - start) / 100 * 1e6

        #time Binary Search (5000 runs - searching is fast)
        start = time.perf_counter()
        for _ in range(5000):
            binary_search(sorted_sub, target)
        search_avg = (time.perf_counter() - start) / 5000 * 1e6

        sort_times.append(sort_avg)
        search_times.append(search_avg)
        print(f"{n:<12}{sort_avg:<20.4f}{search_avg:<18.4f}")
    print("-" * 50)
    print("Merge Sort is O(n log n), Binary Search is O(log n).")

    plt.figure(figsize=(8, 5))
    plt.plot(data_sizes, sort_times, marker="o", label="Merge Sort O(n log n)")
    plt.plot(data_sizes, search_times, marker="o", label="Binary Search O(log n)")
    plt.title("Merge Sort vs Binary Search")
    plt.xlabel("Number of Records")
    plt.ylabel("Average Time (µs)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("q2_sort_vs_search.png", dpi=300)
    plt.show()