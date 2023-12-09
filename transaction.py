class InMemoryDB:
    def __init__(self):
        self.data = {}
        self.transaction_stack = []
        self.isCommit = False
    def get(self, key):
        if(self.isCommit == True):
            self.isCommit == False
            return self.data.get(key, None)
        else:
            return None
        

    def put(self, key, val):
        if not self.transaction_stack:
            raise RuntimeError("No transaction in progress")
        self.data[key] = val

    def begin_transaction(self):
        self.transaction_stack.append(self.data.copy())

    def commit(self):
        if not self.transaction_stack:
            raise RuntimeError("No transaction to commit")
        self.isCommit = True
        self.transaction_stack.pop()

    def rollback(self):
        if not self.transaction_stack:
            raise RuntimeError("No ongoing transaction")

        self.data = self.transaction_stack.pop()


inmemoryDB = InMemoryDB()

# should return None, because A doesn’t exist in the DB yet
print(inmemoryDB.get("A"))

try:
    # should throw an error because a transaction is not in progress
    inmemoryDB.put("A", 5)
except RuntimeError as e:
    print("Error:", e)

# starts a new transaction
inmemoryDB.begin_transaction()

# set’s value of A to 5, but it's not committed yet
inmemoryDB.put("A", 5)

# should return None, because updates to A are not committed yet
print(inmemoryDB.get("A"))

# update A’s value to 6 within the transaction
inmemoryDB.put("A", 6)

# commits the open transaction
inmemoryDB.commit()

# should return 6, that was the last value of A to be committed
print(inmemoryDB.get("A"))

try:
    # throws an error because there is no open transaction
    inmemoryDB.commit()
except RuntimeError as e:
    print("Error:", e)

try:
    # throws an error because there is no ongoing transaction
    inmemoryDB.rollback()
except RuntimeError as e:
    print("Error:", e)

# should return None because B does not exist in the database
print(inmemoryDB.get("B"))

# starts a new transaction
inmemoryDB.begin_transaction()

# Set key B’s value to 10 within the transaction
inmemoryDB.put("B", 10)

# Rollback the transaction - revert any changes made to B
inmemoryDB.rollback()

# Should return None because changes to B were rolled back
print(inmemoryDB.get("B"))

