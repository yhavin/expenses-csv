import sqlite3
from datetime import datetime
from dateutil import parser

import typer
from rich.console import Console
from rich.table import Table


app = typer.Typer()
console = Console()


DB = "expenses.db"
DEFAULT_CATEGORIES = [
    ("Food",),
    ("Transport",),
    ("Travel",),
    ("Home",),
    ("Charity",),
    ("Shopping",),
    ("Other",)
]


def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS expense (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL
            );
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            );
            """
        )
        c.executemany(
            "INSERT OR IGNORE into category (name) VALUES (?)",
            DEFAULT_CATEGORIES
        )
        conn.commit()


def autocomplete_categories(incomplete):
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        # Get all categories in single query since categories are not assumed to be high quantity
        c.execute(
            "SELECT * FROM category"
        )
        categories = c.fetchall()
    return [category[0] for category in categories if category[0].startswith(incomplete)]


@app.command()
def add(
    date: str = typer.Option(datetime.now().strftime("%Y-%m-%d"), prompt="Date"),
    description: str = typer.Option(..., prompt="Description"),
    category: str = typer.Option(..., prompt="Category", autocompletion=autocomplete_categories),
    amount: float = typer.Option(..., prompt="Amount")
):
    """Add a new expense."""
    date = parser.parse(date).strftime("%Y-%m-%d")
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO expense (date, description, category, amount) VALUES (?, ?, ?, ?)", 
            (date, description, category, amount)
        )
        conn.commit()
    console.print("Expense added.")    


@app.command()
def list(page: int = typer.Option(1)):
    """List expenses with pagination."""
    items_per_page = 15
    offset = (page - 1) * items_per_page
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT date, description, category, amount FROM expense ORDER BY date DESC LIMIT ? OFFSET ?",
            (items_per_page, offset)
        )
        expenses = c.fetchall()
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Date")
    table.add_column("Description")
    table.add_column("Category")
    table.add_column("Amount", justify="right")

    for expense in expenses:
        date = datetime.strptime(expense[0], "%Y-%m-%d").strftime("%d-%b-%Y")
        amount = f"{expense[3]:.2f}"
        table.add_row(date, *expense[1:3], amount)
    console.print(table)


if __name__ == "__main__":
    init_db()
    # app()
    typer.run(app)