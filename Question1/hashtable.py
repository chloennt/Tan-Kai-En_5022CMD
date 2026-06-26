class Medicine:
    def __init__(self, product_id, name, med_type, price, quantity):
        self.product_id = product_id   #"M12345678"
        self.name = name               #str
        self.med_type = med_type       #tablet/syrup
        self.price = price             #float
        self.quantity = quantity       #int - stock count

    def __str__(self):
        return (f"ID: {self.product_id},"
                f" Name: {self.name},"
                f" Type: {self.med_type},"
                f" Price: RM{self.price:.2f},"
                f" Qty: {self.quantity}")

class HashTable:
    def __init__(self, size=101):
        self.size = size
        self.slots = [None] * size

    def hash_function(self, key):
        #strip the 'M' prefix, use the number & wrap into table range
        return int(key[1:]) % self.size

    def insert(self, product):
        index = self.hash_function(product.product_id)
        start = index
        first_deleted = -1
        while self.slots[index] is not None:
            #same ID already here, then overwrite it - update instead of duplicate
            if self.slots[index] != "DELETED" and self.slots[index].product_id == product.product_id:
                self.slots[index] = product
                return True
            if self.slots[index] == "DELETED" and first_deleted == -1:
                first_deleted = index
            index = (index + 1) % self.size #linear probe, try next slot
            if index == start: #came full circle = table full
                break
        #place into the earliest tombstone, else the empty slot we landed on
        if first_deleted != -1:
            self.slots[first_deleted] = product
        elif self.slots[index] is None:
            self.slots[index] = product
        else:
            print("Hash table is full.")
            return False
        return True

    def search(self, product_id):
        index = self.hash_function(product_id)
        start = index
        #walk forward over occupied slots until we find it or hit an empty slot
        while self.slots[index] is not None:
            if self.slots[index] != "DELETED" and self.slots[index].product_id == product_id:
                return self.slots[index]
            index = (index + 1) % self.size
            if index == start:
                break
        return None #not found

    def edit(self, product_id, name=None, med_type=None, price=None, quantity=None):
        product = self.search(product_id)
        if product:
            #only overwrite fields the user actually supplied
            if name: product.name = name
            if med_type: product.med_type = med_type
            if price is not None: product.price = price
            if quantity is not None: product.quantity = quantity
            print("Product updated successfully!")
            return True
        print("Product not found.")
        return False

    def delete(self, product_id):
        index = self.hash_function(product_id)
        start = index
        while self.slots[index] is not None:
            if self.slots[index] != "DELETED" and self.slots[index].product_id == product_id:
                #mark as tombstone, NOT None
                self.slots[index] = "DELETED"
                return True
            index = (index + 1) % self.size
            if index == start:
                break
        return False

    def get_all_products(self):
        #actual products only, skip empty and tombstone slots
        return [s for s in self.slots if s is not None and s != "DELETED"]

    def display_items(self):
        for i, slot in enumerate(self.slots):
            if slot is None:
                print(f"Slot {i}: [empty]")
            elif slot == "DELETED":
                print(f"Slot {i}: [deleted]")
            else:
                print(f"Slot {i}: {slot}")