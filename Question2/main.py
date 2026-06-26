from transaction import Transaction
from helpers import (merge_sort, binary_search, linear_search, generate_sample_data, reset_call_count, ask_text, ask_number, compare_search_graph,
                     ask_date, compare_sort_vs_search)
import helpers #to read merge_call_count after sorting
import time
import random

def display_all(data):
    if not data:
        print("No transactions available.")
        return
    for t in data:
        print(t)

def transaction_system():
    data = generate_sample_data(15)
    used_ids = set(t.transaction_id for t in data)

    while True:
        print("\n==================================================")
        print("           Transaction Management System          ")
        print("==================================================")
        print("--- View ---")
        print("1. Display All Transactions")
        print("\n--- Sort ---")
        print("2. Merge Sort (Transaction ID)")
        print("3. Merge Sort (Amount)")
        print("4. Merge Sort (Date)")
        print("\n--- Search ---")
        print("5. Binary Search (Transaction ID)")
        print("6. Linear Search (Transaction ID)")
        print("\n--- Compare ---")
        print("7. Binary Search vs Linear Search (Table + Graph)")
        print("8. Merge Sort vs Binary Search (Table + Graph)")
        print("\n--- Manage ---")
        print("9. Insert Transaction")
        print("\n10. Exit\n")

        while True:
            choice = input("Enter choice: ").strip()
            if choice in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
                break
            print("\nInvalid choice. Please enter 1-10 only.")

        if choice == "1":
            print("\n=========================================================================================")
            print("                                     All Transactions                                    ")
            print("=========================================================================================")
            display_all(data)

        elif choice == "2":
            print("\n==================================================")
            print("              Sort by ID (Merge Sort)             ")
            print("==================================================")
            print("Before sorting:")
            display_all(data)
            reset_call_count() #count recursive calls
            data = merge_sort(data, key="transaction_id")
            print("\nAfter sorting (by ID):")
            display_all(data)
            print(f"\nMerge Sort recursive calls: {helpers.merge_call_count}")

        elif choice == "3":
            print("\n==================================================")
            print("            Sort by Amount (Merge Sort)           ")
            print("==================================================")
            print("Before sorting:")
            display_all(data)
            reset_call_count()
            data = merge_sort(data, key="amount")
            print("\nAfter sorting (by amount, low to high):")
            display_all(data)
            print(f"\nMerge Sort recursive calls: {helpers.merge_call_count}")

        elif choice == "4":
            print("\n==================================================")
            print("             Sort by Date (Merge Sort)            ")
            print("==================================================")
            print("Before sorting:")
            display_all(data)
            reset_call_count()
            data = merge_sort(data, key="transaction_date")
            print("\nAfter sorting (by date, earliest first):")
            display_all(data)
            print(f"\nMerge Sort recursive calls: {helpers.merge_call_count}")

        elif choice == "5":
            print("\n==================================================")
            print("            Search by ID (Binary Search)          ")
            print("==================================================")
            print("(Enter 0 to exit back to menu)\n")
            print("Note: list is sorted by ID before searching.")
            sorted_data = merge_sort(data, key="transaction_id") #binary needs sorted
            while True:
                tid = ask_number("Enter Transaction ID to search: ", is_int=True)
                if tid is None: break #0 = back to menu
                result = binary_search(sorted_data, tid)
                if result:
                    print("\nTransaction Found:")
                    print(result)
                    break
                print("\nTransaction not found. Try again or enter 0 to exit.")

        elif choice == "6":
            print("\n==================================================")
            print("            Search by ID (Linear Search)          ")
            print("==================================================")
            print("(Enter 0 to exit back to menu)\n")
            while True:
                tid = ask_number("Enter Transaction ID to search: ", is_int=True)
                if tid is None: break #0 = back to menu
                result = linear_search(data, tid)
                if result:
                    print("\nTransaction Found:")
                    print(result)
                    break
                print("\nTransaction not found. Try again or enter 0 to exit.")

        elif choice == "7":
            print("\n==================================================")
            print("   Binary Search vs Linear Search (Table+Graph)   ")
            print("==================================================")
            compare_search_graph(data)

        elif choice == "8":
            print("\n==================================================")
            print("    Merge Sort vs Binary Search (Table+Graph)     ")
            print("==================================================")
            compare_sort_vs_search(data)

        elif choice == "9":
            print("\n==================================================")
            print("                Insert Transaction                ")
            print("==================================================")
            print("(Enter 0 to exit back to menu)\n")
            name = ask_text("Enter Customer Name: ")
            if name is None: continue
            product = ask_text("Enter Product Name: ")
            if product is None: continue
            amount = ask_number("Enter Amount: ", max_val=100000)
            if amount is None: continue
            date = ask_date("Enter Date (YYYY-MM-DD): ")
            if date is None: continue
            #auto-generate a unique ID
            while True:
                tid = random.randint(1000, 9999)
                if tid not in used_ids:
                    used_ids.add(tid)
                    break
            data.append(Transaction(tid, name, product, amount, date))
            print(f"\nTransaction inserted! Assigned ID: {tid}")

        elif choice == "10":
            print("\n==================================================")
            print("                     Exiting                      ")
            print("==================================================")
            break

if __name__ == "__main__":
    transaction_system()