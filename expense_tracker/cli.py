from typing import Optional
import typer
from . import __app_name__, __version__, config, ERRORS, DB_READ_ERROR, DB_WRITE_ERROR, db
import rich
from rich.table import Table
from pathlib import Path
from .db import Database
from .api import ExpenseAPI

app = typer.Typer()


@app.command()
def init(
    db_path: str = typer.Option(
        str(db.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="expense database path?"
    ),
) -> None:
    """
    Initialize the expense tracker app.
    """
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f"Error initializing the app: {ERRORS[app_init_error]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    db = Database()
    db_init_error = db.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f"Error initializing the database: {ERRORS[db_init_error]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"Database initialized successfully with db path {db_path}.", fg=typer.colors.GREEN)
        typer.secho("App initialized successfully.", fg=typer.colors.GREEN)
        
@app.command()
def add(
    name: str = typer.Option(..., "-n", "--name", prompt="Expense name?"),
    description: str = typer.Option(..., "-d", "--description", prompt="Expense description?"),
    price : int = typer.Option(..., "-p", "--price", prompt="Expense price?"),
) -> None:
    """
    Add an expense to the expense tracker app.
    """
    
    if config.CONFIG_FILE_PATH.exists() == False:
        typer.secho(
            'Config file not found. Please, run "expense init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    expense_api = ExpenseAPI();
    expense_response = expense_api.add_expense(name, description, price)
    
    if expense_response.error:
        typer.secho(
            f"Error adding expense: {ERRORS[expense_response.error]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"Expense added successfully.", fg=typer.colors.GREEN)

@app.command()
def update(
    id: int = typer.Option(..., prompt="Expense id?"),
    name: str = typer.Option(None,  "-n", "--name"),
    description: str = typer.Option(None,  "-d", "--description"),
    price : int = typer.Option(None,  "-p", "--price"),
) -> None:
    """
    Update an expense in the expense tracker app.
    """
    
    if config.CONFIG_FILE_PATH.exists() == False:
        typer.secho(
            'Config file not found. Please, run "expense init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    
    expense_api = ExpenseAPI();
    expense_response = expense_api.update_expense(id, name, description, price)
    
    if expense_response.error:
        typer.secho(
            f"Error updating expense: {ERRORS[expense_response.error]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"Expense updated successfully.", fg=typer.colors.GREEN)
        
@app.command()
def delete(
    id: int = typer.Option(..., prompt="Expense id?")
) -> None:
    """
    Delete an expense from the expense tracker app.
    """
    
    if config.CONFIG_FILE_PATH.exists() == False:
        typer.secho(
            'Config file not found. Please, run "expense init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    
    expense_api = ExpenseAPI();
    expense_response = expense_api.remove_expense(id)
    
    if expense_response.error:
        typer.secho(
            f"Error deleting expense: {ERRORS[expense_response.error]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"Expense deleted successfully.", fg=typer.colors.GREEN)


@app.command(name="list")
def list_all():
    """
    List all expenses in the expense tracker app.
    """
    if config.CONFIG_FILE_PATH.exists() == False:
        typer.secho(
            'Config file not found. Please, run "expense init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    
    expense_api = ExpenseAPI();
    expense_list = expense_api.read_expenses().expense_list
    if len(expense_list) == 0:
        typer.secho("No expenses found.", fg=typer.colors.GREEN)
        raise typer.Exit()
    
    typer.secho("\nExpense list:\n", fg=typer.colors.BLUE, bold=True)
    table = Table(box=rich.box.SIMPLE)
    table.add_column("Id")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Price")
    for expense in expense_list:
        table.add_row(str(expense.id), expense.name, expense.description, str(expense.price))
    rich.print(table)
    
@app.command()
def total():
    """
    Genarates total expense in the expense tracker app.
    """
    if config.CONFIG_FILE_PATH.exists() == False:
        typer.secho(
            'Config file not found. Please, run "expense init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    expense_api = ExpenseAPI();
    response = expense_api.get_total_expense();
    
    if response == DB_READ_ERROR:
        typer.secho(
            f"Error reading expenses: {ERRORS[response]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"Total expense: {response}", fg=typer.colors.GREEN)

@app.command()
def clear():
    """
    clear all expenses in the expense tracker app.
    """
    expense_api = ExpenseAPI();
    response = expense_api.clear_expenses();
    
    if response == DB_WRITE_ERROR:
        typer.secho(
            f"Error clearing expenses: {ERRORS[response]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"Expenses cleared successfully.", fg=typer.colors.GREEN)
    
    
def __version_callback(value: bool):
    if value:
        typer.echo(f"{__app_name__} version {__version__}")
        raise typer.Exit()
    
@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, 
        "--version",
        "-v",
        help="Shows application version and exit",  
        callback=__version_callback, 
        is_eager=True
    )
) -> None:
    """
    Expense is a small CLI app to track expenses.
    """
    return
