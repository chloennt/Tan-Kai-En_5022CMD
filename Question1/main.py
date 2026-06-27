from hashtable import HashTable, Medicine
from helpers import (generate_random_product_id, generate_sample_data, compare_hash_vs_array, ask_text, ask_number, ask_id)

def inventory_system():
    ht = HashTable(size=101) #prime size spreads keys more evenly
    generate_sample_data(ht, count=10)
    #track used IDs so auto-generated ones never clash
    used_ids = set(p.product_id for p in ht.get_all_products())

    while True:
        print("\n==============================================")
        print("              Pharmacy Inventory              ")
        print("==============================================")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. Display All With Details")
        print("6. Compare Hash Table vs Array (Table+Graph)")
        print("7. Exit\n")

        #keep asking for a valid choice without reprinting the whole menu
        while True:
            choice = input("Enter choice: ").strip()
            if choice in ("1", "2", "3", "4", "5", "6", "7"):
                break
            print("\nInvalid choice. Please enter 1-7 only.")

        if choice == "1":
            print("\n==============================================")
            print("                Insert Product                ")
            print("==============================================")
            print("(Enter 0 to exit back to menu)\n")
            name = ask_text("Enter Product Name: ")
            if name is None: continue
            name = name.title() #capitalize each word
            med_type = ask_text("Enter Product Type: ")
            if med_type is None: continue
            med_type = med_type.title()
            price = ask_number("Enter Price: ")
            if price is None: continue
            qty = ask_number("Enter Quantity: ", is_int=True)
            if qty is None: continue

            pid = generate_random_product_id(used_ids)
            ht.insert(Medicine(pid, name, med_type, price, qty))
            print(f"\nProduct inserted! Assigned ID: {pid}")

        elif choice == "2":
            print("\n======================================================================")
            print("                          Search Product                              ")
            print("======================================================================")
            print("(Enter 0 to exit back to menu)\n")
            pid = ask_id("Enter Product ID (e.g. M12345678): ")
            if pid is None: continue
            result = ht.search(pid)
            print("\nProduct Found:" if result else "Product not found.")
            if result:
                print(result)

        elif choice == "3":
            print("\n======================================================================")
            print("                           Edit Product                               ")
            print("======================================================================")
            print("(Enter 0 to exit back to menu)\n")
            pid = ask_id("Enter Product ID to edit: ")
            if pid is None: continue
            product = ht.search(pid)
            if product:
                print("Editing:")
                print(product)
                #blank input means keep the current value
                nn = input("\nNew name (blank=keep): ")
                nt = input("New type (blank=keep): ")
                np_ = input("New price (blank=keep): ")
                nq = input("New quantity (blank=keep): ")
                try:
                    pv = float(np_) if np_ else None
                    qv = int(nq) if nq else None
                except ValueError:
                    print("\nInvalid numeric value.")
                    continue
                # if user left everything blank, nothing to update
                if not nn and not nt and not np_ and not nq:
                    print("\nNothing changed.")
                else:
                    ht.edit(pid, name=nn.title() if nn else None, med_type=nt.title() if nt else None, price=pv, quantity=qv)
            else:
                print("\nProduct not found.")

        elif choice == "4":
            print("\n==============================================")
            print("                Delete Product                ")
            print("==============================================")
            print("(Enter 0 to exit back to menu)\n")
            while True:
                pid = ask_id("Enter Product ID to delete: ")
                if pid is None: break #0 = back to menu
                if ht.delete(pid):
                    used_ids.discard(pid) #free the ID for reuse
                    print("\nProduct deleted successfully!")
                    break
                print("\nProduct not found. Please try again.")

        elif choice == "5":
            print("\n=========================================================================================")
            print("                               Display All with Details                                  ")
            print("=========================================================================================")
            ht.display_items()

        elif choice == "6":
            print("\n==============================================")
            print("      Hash Table vs Array (Table+Graph)       ")
            print("==============================================")
            compare_hash_vs_array(ht)

        elif choice == "7":
            print("\n==============================================")
            print("                   Exiting                    ")
            print("==============================================")
            break

if __name__ == "__main__":
    inventory_system()
