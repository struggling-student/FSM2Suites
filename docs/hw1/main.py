import unittest
from typing import List, Dict, Any


class Account:
    def __init__(self, name: str, balance: float = 0.0):
        self.name = name
        self.balance = balance

    def deposit(self, amount: float) -> bool:
        if amount < 0:
            return False
        self.balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        if amount < 0 or self.balance < amount:
            return False
        self.balance -= amount
        return True

    def __str__(self):
        return f"{self.name}: {self.balance:.2f}"


class Transaction:
    def __init__(self):
        self.descriptions: Dict[str, List[str]] = {}
        self.data: Dict[str, List[List[int]]] = {}

    def extract_args(self, args: List[Any], indices: List[int]) -> List[Any]:
        return [args[i] for i in indices]

    def prepare(self, operation_name: str, args: List[Any]) -> bool:
        method = getattr(args[0], operation_name, None)
        if method is None:
            return False
        return method(*args[1:])

    def rollback(self, done: List[tuple[str, List[Any]]]):
        print("ROLLBACK:", done)
        # Undo the operations that were already completed, in reverse order
        for op, args in reversed(done):
            if op == "deposit":
                # Undo deposit by withdrawing the same amount
                account = args[0]
                amount = args[1]
                account.withdraw(amount)
            elif op == "withdraw":
                # Undo withdraw by depositing the same amount back
                account = args[0]
                amount = args[1]
                account.deposit(amount)

    def commit(self, done: Dict[str, List[Any]]):
        print("COMMIT:", done)

    def exec_trans(self, trans_name: str, args: List[Any]) -> bool:
        done: List[tuple[str, List[Any]]] = []  # Track successful operations in order

        for op, index_set in zip(self.descriptions[trans_name], self.data[trans_name]):
            to_do_args = self.extract_args(args, index_set)
            success = self.prepare(op, to_do_args)
            if success:
                done.append((op, to_do_args))
            else:
                self.rollback(done)
                return False

        self.commit(dict(done))
        return True

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.acc1 = Account("Customer", 100.0)
        self.acc2 = Account("Receiver", 50.0)
        self.trans = Transaction()

        # In-memory description and data (no files)
        self.trans.descriptions = {
            "transfer": ["deposit", "withdraw"]
        }
        self.trans.data = {
            "transfer": [[1, 0], [2, 0]]  # acc2.deposit(amount), acc1.withdraw(amount)
        }

    def test_successful_transfer(self):
        result = self.trans.exec_trans("transfer", [30.0, self.acc2, self.acc1])
        self.assertTrue(result)
        self.assertEqual(self.acc1.balance, 70.0)
        self.assertEqual(self.acc2.balance, 80.0)

    def test_insufficient_funds(self):
        result = self.trans.exec_trans("transfer", [130.0, self.acc2, self.acc1])
        self.assertFalse(result)
        self.assertEqual(self.acc1.balance, 100.0)
        self.assertEqual(self.acc2.balance, 50.0)

    def test_negative_deposit(self):
        # Set up a faulty transaction: first operation tries to deposit a negative amount
        self.trans.descriptions["bad_transfer"] = ["deposit", "withdraw"]
        self.trans.data["bad_transfer"] = [[1, 0], [2, 0]]
        result = self.trans.exec_trans("bad_transfer", [-10.0, self.acc2, self.acc1])
        self.assertFalse(result)
        self.assertEqual(self.acc1.balance, 100.0)
        self.assertEqual(self.acc2.balance, 50.0)

    def test_atomic_transaction_partial_failure(self):
        """Test that if any operation in a transaction fails, all previous operations are rolled back"""
        # Create an account with insufficient funds for the second operation
        acc3 = Account("LimitedFunds", 20.0)
        
        # Set up a multi-step transaction: deposit to acc2, then withdraw large amount from acc3
        self.trans.descriptions["multi_step"] = ["deposit", "withdraw"]
        self.trans.data["multi_step"] = [[1, 0], [2, 0]]  # acc2.deposit(amount), acc3.withdraw(amount)
        
        # Record initial balances
        initial_acc2_balance = self.acc2.balance
        initial_acc3_balance = acc3.balance
        
        # Execute transaction that should fail on second operation
        result = self.trans.exec_trans("multi_step", [50.0, self.acc2, acc3])
        
        # Transaction should fail
        self.assertFalse(result)
        
        # All balances should be unchanged (atomicity preserved)
        self.assertEqual(self.acc2.balance, initial_acc2_balance)
        self.assertEqual(acc3.balance, initial_acc3_balance)

    def test_atomic_transaction_complex_rollback(self):
        """Test atomic rollback with multiple successful operations before failure"""
        acc4 = Account("TempAccount", 100.0)
        acc5 = Account("FinalAccount", 10.0)  # Insufficient for final large withdrawal
        
        # Complex transaction: multiple operations, with final operation failing
        self.trans.descriptions["complex_trans"] = ["deposit", "withdraw", "deposit", "withdraw"]
        self.trans.data["complex_trans"] = [
            [1, 0],  # acc4.deposit(amount - 25.0)
            [2, 0],  # self.acc1.withdraw(amount - 25.0) 
            [3, 0],  # acc5.deposit(amount - 25.0)
            [3, 4]   # acc5.withdraw(large_amount - 100.0) - this should fail
        ]
        
        # Record initial balances
        initial_acc1_balance = self.acc1.balance
        initial_acc4_balance = acc4.balance
        initial_acc5_balance = acc5.balance
        
        # Execute transaction with different amounts: first 3 operations use 25.0, last uses 100.0
        result = self.trans.exec_trans("complex_trans", [25.0, acc4, self.acc1, acc5, 100.0])
        
        # Transaction should fail due to insufficient funds in final withdrawal
        self.assertFalse(result)
        
        # All accounts should have their original balances (full rollback)
        self.assertEqual(self.acc1.balance, initial_acc1_balance)
        self.assertEqual(acc4.balance, initial_acc4_balance)
        self.assertEqual(acc5.balance, initial_acc5_balance)

    def test_atomic_all_or_nothing_principle(self):
        """Test that transactions follow all-or-nothing principle"""
        # Create accounts for testing
        source = Account("Source", 1000.0)
        intermediate = Account("Intermediate", 0.0)
        destination = Account("Destination", 0.0)
        
        # Multi-step transaction chain
        self.trans.descriptions["chain_transfer"] = ["withdraw", "deposit", "withdraw", "deposit"]
        self.trans.data["chain_transfer"] = [
            [0, 1],  # source.withdraw(amount)
            [2, 1],  # intermediate.deposit(amount)
            [2, 1],  # intermediate.withdraw(amount)
            [3, 1]   # destination.deposit(amount)
        ]
        
        # Test successful chain transfer
        result = self.trans.exec_trans("chain_transfer", [source, 100.0, intermediate, destination])
        self.assertTrue(result)
        self.assertEqual(source.balance, 900.0)
        self.assertEqual(destination.balance, 100.0)
        
        # Reset for failure test
        source.balance = 500.0  # Reduce balance to cause failure
        intermediate.balance = 0.0
        destination.balance = 0.0
        
        # Test transaction that will fail due to insufficient funds
        result2 = self.trans.exec_trans("chain_transfer", [source, 600.0, intermediate, destination])
        
        # Should fail and all accounts should be unchanged from reset state
        self.assertFalse(result2)
        self.assertEqual(source.balance, 500.0)
        self.assertEqual(intermediate.balance, 0.0)
        self.assertEqual(destination.balance, 0.0)

    def test_transaction_isolation_simulation(self):
        """Simulate concurrent transaction scenario to test atomicity"""
        # This simulates what would happen if two transactions tried to access the same accounts
        shared_account = Account("SharedAccount", 100.0)
        user1_account = Account("User1", 50.0)
        user2_account = Account("User2", 75.0)
        
        # Transaction 1: Transfer from shared to user1
        self.trans.descriptions["transfer1"] = ["withdraw", "deposit"]
        self.trans.data["transfer1"] = [[0, 1], [2, 1]]  # shared.withdraw, user1.deposit
        
        # Transaction 2: Transfer from shared to user2  
        self.trans.descriptions["transfer2"] = ["withdraw", "deposit"]
        self.trans.data["transfer2"] = [[0, 1], [2, 1]]  # shared.withdraw, user2.deposit
        
        # Execute first transaction
        result1 = self.trans.exec_trans("transfer1", [shared_account, 60.0, user1_account])
        self.assertTrue(result1)
        
        # After first transaction
        self.assertEqual(shared_account.balance, 40.0)
        self.assertEqual(user1_account.balance, 110.0)
        
        # Execute second transaction (should fail due to insufficient funds)
        result2 = self.trans.exec_trans("transfer2", [shared_account, 60.0, user2_account])
        self.assertFalse(result2)
        
        # Shared account and user2 should be unchanged after failed transaction
        self.assertEqual(shared_account.balance, 40.0)  # Still 40 from first transaction
        self.assertEqual(user2_account.balance, 75.0)   # Unchanged due to failed transaction

    def test_atomicity_with_side_effects_verification(self):
        """Comprehensive test to verify true atomicity - no partial state changes"""
        # Create a scenario where we can verify that intermediate states don't persist
        bank = Account("Bank", 1000.0)
        customer1 = Account("Customer1", 200.0)
        customer2 = Account("Customer2", 150.0)
        customer3 = Account("Customer3", 5.0)  # Will cause the transaction to fail
        
        # Record all initial balances
        initial_balances = {
            'bank': bank.balance,
            'customer1': customer1.balance,
            'customer2': customer2.balance,
            'customer3': customer3.balance
        }
        
        # Complex multi-step transaction that will fail at the last step
        self.trans.descriptions["complex_banking"] = [
            "withdraw",  # Bank withdraws money
            "deposit",   # Customer1 receives money
            "withdraw",  # Customer1 transfers some to Customer2
            "deposit",   # Customer2 receives money
            "withdraw",  # Customer2 tries to transfer to Customer3
            "deposit",   # Customer3 receives money
            "withdraw"   # Customer3 tries to withdraw more than available (FAIL)
        ]
        
        self.trans.data["complex_banking"] = [
            [0, 1],  # bank.withdraw(100)
            [2, 1],  # customer1.deposit(100)
            [2, 1],  # customer1.withdraw(100)
            [3, 1],  # customer2.deposit(100) 
            [3, 1],  # customer2.withdraw(100)
            [4, 1],  # customer3.deposit(100)
            [4, 5]   # customer3.withdraw(200) - SHOULD FAIL
        ]
        
        # Execute the transaction that should fail
        result = self.trans.exec_trans("complex_banking", 
                                     [bank, 100.0, customer1, customer2, customer3, 200.0])
        
        # Verify transaction failed
        self.assertFalse(result)
        
        # Verify ALL accounts have exactly their initial balances (true atomicity)
        self.assertEqual(bank.balance, initial_balances['bank'])
        self.assertEqual(customer1.balance, initial_balances['customer1'])
        self.assertEqual(customer2.balance, initial_balances['customer2'])
        self.assertEqual(customer3.balance, initial_balances['customer3'])
        
        # Additional verification: check that no account has any traces of intermediate operations
        self.assertEqual(bank.balance, 1000.0)      # Never changed from initial
        self.assertEqual(customer1.balance, 200.0)  # Never changed from initial
        self.assertEqual(customer2.balance, 150.0)  # Never changed from initial
        self.assertEqual(customer3.balance, 5.0)    # Never changed from initial
