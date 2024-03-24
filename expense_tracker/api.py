"""API module for the app."""
# expense/api.py
from dataclasses import asdict, dataclass
import json
from pathlib import Path

from .db import Database
from . import config

from . import DB_READ_ERROR, DB_WRITE_ERROR, ITEM_NOT_FOUND_ERROR, JSON_ERROR, SUCCESS

@dataclass
class Expense():
    """
    Expense dataclass.
    """
    id: int
    name: str
    description: str
    price: int
    
    def __init__(self, id: int, name: str, description: str, price: int) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.price = price
    
    @classmethod
    def from_dict(cls, d : dict):
        return Expense(**d)
    
    def to_dict(self):
        return asdict(self)

class ExpenseResponse():
    """
    Expense response.
    """
    expense_list : list[Expense] = []
    error : int
    
    def __init__(self, expense_list, error) -> None:
        self.expense_list = expense_list
        self.error = error
    

class ExpenseAPI():
    """
    Expense api class
    """
    def __init__(self, db_path: Path = None) -> None:
        db = Database()
        self._db_path = db_path if db_path is not None else db.get_database_path(config.CONFIG_FILE_PATH)
        
    def read_expenses(self) -> ExpenseResponse:
        """
        Read expenses from the database.
        """
        try:
            db = Database()
            response = db.read_database(self._db_path)            
            return ExpenseResponse(json.loads(response, object_hook= lambda d: Expense.from_dict(d)), 0)
        except OSError:
            return ExpenseResponse([], DB_READ_ERROR)   
    
    def write_expenses(self, expenses: list[Expense]) -> ExpenseResponse:
        """
        Write expenses to the database.
        """
        try:
            db = Database()
            db.write_database(self._db_path, [expense.to_dict() for expense in expenses])
            return ExpenseResponse(expenses, SUCCESS)
        except OSError:
            return ExpenseResponse([], DB_WRITE_ERROR)
 
    def add_expense(self, name: str, description: str, price: int) -> ExpenseResponse:
        """
        Add an expense to the database.
        """
        expenses_response = self.read_expenses()
        if expenses_response.error == DB_READ_ERROR:
            return expenses_response
        
        id = 1 if len(expenses_response.expense_list) == 0 else max([expense.id for expense in expenses_response.expense_list]) + 1
        expense = Expense(id, name, description, price)
        expenses_response.expense_list.append(expense)
        return self.write_expenses(expenses_response.expense_list)
    
    def update_expense(self, id: int, name: str, description: str, price: int) -> ExpenseResponse:
        """
        Update an expense in the database.
        """
        expenses_response = self.read_expenses()
        if expenses_response.error == DB_READ_ERROR:
            return expenses_response
        
        expense_found = next((expense for expense in expenses_response.expense_list if expense.id == id), None)
        
        if expense_found is None:
            return ExpenseResponse([], ITEM_NOT_FOUND_ERROR)
        
        result = []
        
        for expense in expenses_response.expense_list:
            if expense.id == id:
                expense.name = name if name is not None else expense.name
                expense.description = description if description is not None else expense.description
                expense.price = price if price is not None else expense.price
            result.append(expense)
        
        return self.write_expenses(result)
    
    def remove_expense(self, id: int) -> ExpenseResponse:
        """
        Remove an expense from the database.
        """
        expenses_response = self.read_expenses()
        if expenses_response.error == DB_READ_ERROR:
            return expenses_response
        
        expense_found = next((expense for expense in expenses_response.expense_list if expense.id == id), None)
        
        if expense_found is None:
            return ExpenseResponse([], ITEM_NOT_FOUND_ERROR)
        
        result = [expense for expense in expenses_response.expense_list if expense.id != id]
        expenses_response.expense_list = result
        return self.write_expenses(expenses_response.expense_list)
    
    def get_total_expense(self) -> int:
        """
        Get the total expense.
        """
        expenses_response = self.read_expenses()
        if expenses_response.error == DB_READ_ERROR:
            return expenses_response.error
        
        return sum([expense.price for expense in expenses_response.expense_list])
    
    def clear_expenses(self) -> ExpenseResponse:
        """
        Clear all expenses.
        """
        return self.write_expenses([])  