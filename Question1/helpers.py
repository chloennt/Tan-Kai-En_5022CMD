#ID generator, sample data, and the performance experiment
import time
import random
import matplotlib.pyplot as plt
from hashtable import Medicine

def is_valid_id(pid):
    #must be 'M' followed by exactly 8 digits
    return len(pid) == 9 and pid[0] == "M" and pid[1:].isdigit()

def ask_text(prompt):
    #keep asking until non-empty, or 0 to cancel
    while True:
        val = input(prompt).strip()
        if val == "0":
            return None
        if val:
            return val
        print("\nThis field cannot be empty.")

def ask_number(prompt, is_int=False):
    #keep asking until a valid non-negative number, or 0 to cancel
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
        return num

def ask_id(prompt):
    #keep asking until a valid ID format, or 0 to cancel
    while True:
        val = input(prompt).strip().upper()
        if val == "0":
            return None
        if is_valid_id(val):
            return val
        print("\nInvalid ID format. Use M followed by 8 digits.")

def generate_random_product_id(existing_ids):
    #make a unique ID like 'M12345678', avoiding duplication
    while True:
        pid = f"M{random.randint(10000000, 99999999)}"
        if pid not in existing_ids:
            existing_ids.add(pid)
            return pid

def generate_sample_data(ht, count=10):
    catalog = {
        "Tablet":     ["Paracetamol", "Ibuprofen", "Aspirin"],
        "Syrup":      ["Cough Syrup", "Antacid Syrup", "Vitamin Syrup"],
        "Supplement": ["Vitamin C", "Fish Oil", "Calcium Tablet"],
        "Capsule":    ["Amoxicillin", "Omega 3", "Probiotic"],
        "Ointment":   ["Antiseptic Cream", "Burn Gel", "Muscle Rub"],
    }
    used_ids = set()
    #flatten catalog into (type, name) pairs to pick from randomly
    all_products = [(t, n) for t, names in catalog.items() for n in names]
    for _ in range(count):
        med_type, name = random.choice(all_products)
        price = round(random.uniform(5, 80), 2)
        qty = random.randint(10, 100)
        pid = generate_random_product_id(used_ids)
        ht.insert(Medicine(pid, name, med_type, price, qty))

def compare_hash_vs_array(ht):
    array_data = ht.get_all_products()
    if not array_data:
        print("\nNo data available. Insert records first.")
        return

    #top both structures up to 90 records (under table size 101 to avoid overflow)
    existing_ids = set(p.product_id for p in array_data)
    while len(array_data) < 90:
        pid = generate_random_product_id(existing_ids)
        p = Medicine(pid, "Sample", "Tablet", 9.99, 50)
        array_data.append(p)
        ht.insert(p)

    data_sizes = [10, 20, 40, 60, 80, 90]
    ht_times, arr_times = [], []

    print(f"{'Data Size':<12}{'Hash Table (µs)':<20}{'Array (µs)':<15}")
    print("-" * 47)

    for n in data_sizes:
        subset = array_data[:n]
        target = subset[-1].product_id #last item = worst case for the array

        #hash table: average of 1000 searches, converted to microseconds
        start = time.perf_counter()
        for _ in range(1000):
            ht.search(target)
        ht_avg = (time.perf_counter() - start) / 1000 * 1e6

        #array: linear scan until the ID matches
        start = time.perf_counter()
        for _ in range(1000):
            for item in subset:
                if item.product_id == target:
                    break
        arr_avg = (time.perf_counter() - start) / 1000 * 1e6

        ht_times.append(ht_avg)
        arr_times.append(arr_avg)
        print(f"{n:<12}{ht_avg:<20.4f}{arr_avg:<15.4f}")
    print("-" * 47)

    #plot both curves: hash table stays flat (O(1)), array rises (O(n))
    plt.figure(figsize=(8, 5))
    plt.plot(data_sizes, ht_times, marker="o", label="Hash Table O(1)")
    plt.plot(data_sizes, arr_times, marker="o", label="Array O(n)")
    plt.title("Hash Table (Linear Probing) vs Array Search")
    plt.xlabel("Number of Records")
    plt.ylabel("Average Search Time (µs)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("q1_performance.png", dpi=300)
    plt.show()
