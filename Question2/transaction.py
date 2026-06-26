class Transaction:
    def __init__(self, transaction_id, customer_name, product_name, amount, transaction_date):
        self.transaction_id = transaction_id      #int - unique key, sorted on this
        self.customer_name = customer_name        #str
        self.product_name = product_name          #str
        self.amount = amount                      #float - RM
        self.transaction_date = transaction_date  #str - "YYYY-MM-DD"

    def __str__(self):
        return (f"ID: {self.transaction_id},"
                f" Customer: {self.customer_name},"
                f" Product: {self.product_name},"
                f" Amount: RM{self.amount:.2f},"
                f" Date: {self.transaction_date}")