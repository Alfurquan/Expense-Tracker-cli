expense
=====

Expense tracking command line application.

Getting started
----------
This project is created using Poetry. For more information about poetry refer [here](https://python-poetry.org/)

To get started with Expense tracker, follow these steps:

1. Clone this repository to your local machine.
2. Go inside the cloned repository at `.\expense-tracker\` location.
3. Run `poetry install` to install dependencies and activate virtual environment.
4. Run `poetry shell` to launch the virtual environment shell. 
5. Start running the commands in the usage section to try out.

Usage
-----

Here's a demo of how it works:
    
    # Initialize the app
    $ expense init 

    $ expense add --name "Milk" --description "Bought milk" --price 50

    $ expense add --name "Tea" --description "Bought tea" --price 100
    $ expense list
         ╷       ╷             ╷
      ID │ Name  │ Description │ Price
    ╺━━━━┿━━━━━━━┿━━━━━━━━━━━━━┿━━━━━━━━━━━━━━╸
      1  │ Milk  │ Bought milk │ 50
      2  │ Tea   | Bought tea  │ 100
         ╵       ╵             ╵

    $ expense update --id 1 --price 60

    $ expense delete --id 1

     $ expense list
         ╷       ╷             ╷
      ID │ Name  │ Description │ Price
    ╺━━━━┿━━━━━━━┿━━━━━━━━━━━━━┿━━━━━━━━━━━━━━╸
      2  │ Tea   | Bought tea  │ 100
         ╵       ╵             ╵

    $ expense --help
    Usage: expense [OPTIONS] COMMAND [ARGS]...

      expense is a small CLI app to track expenses.

    Options:
       -v, --version Shows application version and exit
  

    Commands:
      add      Add an expense to the expense tracker app.
      clear   clear all expenses in the expense tracker app.
      delete   Delete an expense from the expense tracker app.
      init     Initialize the expense tracker app.
      list     List all expenses in the expense tracker app.
      total    Generates total expense in the expense tracker app.
      update    Update an expense in the expense tracker app.
