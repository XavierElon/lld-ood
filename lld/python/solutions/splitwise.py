# Singleton Pattern
# The SplitwiseService class is implemented as a Singleton, ensuring that only one instance of the service exists. 
# This is done using a combination of a class-level _instance attribute and a custom __new__ method.

# Polymorphism / Strategy-Like Approach
# The Split class is an abstract base class (ABC), with different concrete implementations: EqualSplit, ExactSplit, and PercentSplit.
# Although this is not strictly the classic Strategy pattern (because the "context" for choosing the split type is the Expense class), it’s still a good example of polymorphism, where each subclass has its own logic for computing get_amount().

# Encapsulation
# Each class is responsible for managing a clear set of data and operations: User manages user data and balances, Group manages members and expenses, Expense manages the details of a particular expense, etc. This leads to a more maintainable design.

import math
from abc import ABC, abstractmethod
from typing import List, Dict

class User:
    def __init__(self, user_id: str, name: str, email: str):
        self.id = user_id
        self.name = name
        self.email = email
        self.balances: Dict[str, float] = {}
        
    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name
    
    def get_email(self) -> str:
        return self.email
    
    def get_balances(self) -> Dict[str, float]:
        return self.balances
    
class Split(ABC):
    def __init__(self, user: User):
        self.user = user
        self.amount = 0.0
        
    @abstractmethod
    def get_amount(self) -> float:
        pass
    
    def set_amount(self, amount: float):
        self.amount = amount
        
    def get_user(self) -> User:
        return self.user
    
class EqualSplit(Split):
    def __init__(self, user: User):
        super().__init__(user)
        
    def get_amount(self) -> float:
        return self.amount
    
class ExactSplit(Split):
    def __init__(self, user: User, amount: float):
        super().__init__(user)
        self.amount = amount
        
    def get_amount(self) -> float:
        return self.amount

class PercentSplit(Split):
    def __init__(self, user: User, percent: float):
        super().__init__(user)
        self.percent = percent
    
    def get_amount(self) -> float:
        return self.amount
    
    def get_percent(self) -> float:
        return self.percent
    
class Expense:
    def __init__(self, expense_id: str, amount: float, description: str, paid_by: User):
        self.id = expense_id
        self.amount = amount
        self.description = description
        self.paid_by = paid_by
        self.splits: List[Split] = []
        
    def add_split(self, split: Split):
        self.splits.append(split)
        
    def get_id(self) -> str:
        return self.id
    
    def get_amount(self) -> float:
        return self.amount
    
    def get_description(self) -> str:
        return self.description
    
    def get_paid_by(self) -> User:
        return self.paid_by

    def get_splits(self) -> List[Split]:
        return self.splits

class Group:
    """
    Represents a group of users (e.g., "Roommates").
    It maintains a list of members and a list of expenses.
    """
    def __init__(self, group_id: str, name: str):
        self.id = group_id
        self.name = name
        self.members: List[User] = []
        self.expenses: List[Expense] = []

    def add_member(self, user: User):
        self.members.append(user)

    def add_expense(self, expense: Expense):
        self.expenses.append(expense)

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_members(self) -> List[User]:
        return self.members

    def get_expenses(self) -> List[Expense]:
        return self.expenses
    
class Transaction:
    """
    Represents a settlement transaction from one user to another
    for a specified amount.
    """
    def __init__(self, transaction_id: str, sender: User, receiver: User, amount: float):
        self.id = transaction_id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        
class SplitwiseService:
    _instance = None
    _TRANSACTION_ID_PREFIX = 'TXN'
    _transaction_counter = 0
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.users: Dict[str, User] = {}
            cls._instance.groups: Dict[str, Group] = {}
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._isntance = cls()
        return cls._instance
    
    def add_user(self, user: User):
        self.users[user.get_id()] = user

    def add_group(self, group: Group):
        self.groups[group.get_id()] = group

    def add_expense(self, group_id: str, expense: Expense):
        group = self.groups.get(group_id)
        if group:
            group.add_expense(expense)
            self._split_expense(expense)   # Determine how much each user owes
            self._update_balances(expense) # Update each user's balances

    def _split_expense(self, expense: Expense):
        total_amount = expense.get_amount()
        splits = expense.get_splits()

        # If you have different types of splits in the same expense,
        # you need a more robust calculation. For demonstration,
        # let's handle only EqualSplit and PercentSplit as shown.
        # (ExactSplit can also be handled similarly or combined.)
        total_percentage = 0
        equal_splits_count = 0

        for split in splits:
            if isinstance(split, PercentSplit):
                total_percentage += split.get_percent()
            elif isinstance(split, EqualSplit):
                equal_splits_count += 1

        # Amount to be assigned for percent splits
        running_amount = total_amount
        for split in splits:
            if isinstance(split, PercentSplit):
                split_amount = (split.get_percent() / 100.0) * total_amount
                split.set_amount(split_amount)
                running_amount -= split_amount

        # Now distribute the remaining among the EqualSplit users
        if equal_splits_count > 0:
            split_amount = running_amount / equal_splits_count
            for split in splits:
                if isinstance(split, EqualSplit):
                    split.set_amount(split_amount)

    def _update_balances(self, expense: Expense):
        paid_by = expense.get_paid_by()
        for split in expense.get_splits():
            user = split.get_user()
            amount = split.get_amount()

            if paid_by != user:
                # user owes 'amount' to paid_by
                self._update_balance(paid_by, user, amount)
                self._update_balance(user, paid_by, -amount)
    
    def _update_balance(self, user1: User, user2: User, amount: float):
        key = self._get_balance_key(user1, user2)
        user1.get_balances()[key] = user1.get_balances().get(key, 0.0) + amount
    
    def _get_balance_key(self, user1: User, user2: User) -> str:
        return f"{user1.get_id()}:{user2.get_id()}"

    def settle_balance(self, user_id1: str, user_id2: str):
        """
        Settles the balance between two users (user_id1 and user_id2).
        Creates a transaction for the owed amount and resets their mutual balance to 0.
        """
        user1 = self.users.get(user_id1)
        user2 = self.users.get(user_id2)

        if user1 and user2:
            key = self._get_balance_key(user1, user2)
            balance = user1.get_balances().get(key, 0.0)

            if math.isclose(balance, 0.0, abs_tol=1e-9):
                return  # Nothing to settle

            if balance > 0:
                # user2 owes user1
                self._create_transaction(user2, user1, balance)
                user1.get_balances()[key] = 0.0
                user2.get_balances()[self._get_balance_key(user2, user1)] = 0.0
            elif balance < 0:
                # user1 owes user2
                self._create_transaction(user1, user2, abs(balance))
                user1.get_balances()[key] = 0.0
                user2.get_balances()[self._get_balance_key(user2, user1)] = 0.0

    def _create_transaction(self, sender: User, receiver: User, amount: float):
        transaction_id = self._generate_transaction_id()
        transaction = Transaction(transaction_id, sender, receiver, amount)
        # Here you could add logic to record the transaction, etc.
        print(f"Transaction {transaction.id}: {sender.get_name()} pays {receiver.get_name()} {amount}")

    def _generate_transaction_id(self) -> str:
        self._transaction_counter += 1
        return f"{self._TRANSACTION_ID_PREFIX}{self._transaction_counter:06d}"

class SplitwiseDemo:
    @staticmethod
    def run():
        splitwise_service = SplitwiseService.get_instance()
        
        user1 = User("1", "Alice", "alice@example.com")
        user2 = User("2", "Bob", "bob@example.com")
        user3 = User("3", "Charlie", "charlie@example.com")

        splitwise_service.add_user(user1)
        splitwise_service.add_user(user2)
        splitwise_service.add_user(user3)
        
        # Create a group
        group = Group("1", "Apartment")
        group.add_member(user1)
        group.add_member(user2)
        group.add_member(user3)

        splitwise_service.add_group(group)
        
         # Add an expense
        expense = Expense("1", 300.0, "Rent", user1)

        # Splits: 2 equal splits and 1 percentage split
        equal_split1 = EqualSplit(user1)
        equal_split2 = EqualSplit(user2)
        percent_split = PercentSplit(user3, 20.0)  # 20% of 300 -> $60
        
        expense.add_split(equal_split1)
        expense.add_split(equal_split2)
        expense.add_split(percent_split)

        # Add the expense to the group (automatically calculates how much each user owes)
        splitwise_service.add_expense(group.get_id(), expense)
        
        splitwise_service.add_expense(group.get_id(), expense)
        
        splitwise_service.settle_balance(user1.get_id(), user2.get_id())
        splitwise_service.settle_balance(user1.get_id(), user3.get_id())
        
        print("\n--- Final Balances ---")
        for user in [user1, user2, user3]:
            print(f"User: {user.get_name()}")
            for key, value in user.get_balances().items():
                if not math.isclose(value, 0.0, abs_tol=1e-9):
                    print(f" Balnace with {key}: {value}")
                    

if __name__ == "__main__":
    SplitwiseDemo.run()