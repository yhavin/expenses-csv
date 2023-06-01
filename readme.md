# About
Easy-to-use command line interface app for tracking expenses and viewing summaries.

# Capabilities
1. Create new expenses file or open pre-exisiting file
2. Add new expenses (date, category, description, amount)
3. Delete expenses
4. View summary by expense category
5. View summary by expense month-year
6. Export summaries to CSV

# Installation
Download `main.py` and run it from the terminal.

# File management
- Expense files are saved as CSVs in the same folder as `main.py`.
- Summaries are exported as CSVs in the same folder as `main.py`.

# Examples
## List of expenses
```
+------+------------+---------------+---------------+----------+
|   Id | Date       | Category      | Description   |   Amount |
+======+============+===============+===============+==========+
|    1 | 2023-06-03 | Food          | Milk          |     5.00 |
+------+------------+---------------+---------------+----------+
|    2 | 2023-06-03 | Travel        | Gas           |    34.67 |
+------+------------+---------------+---------------+----------+
|    3 | 2023-06-04 | Subscriptions | Netflix       |     9.99 |
+------+------------+---------------+---------------+----------+
|    4 | 2023-06-04 | Health        | Gym           |    18.00 |
+------+------------+---------------+---------------+----------+
|    5 | 2023-06-05 | Food          | Groceries     |    86.19 |
+------+------------+---------------+---------------+----------+
|    6 | 2023-06-06 | Travel        | Uber          |     8.80 |
+------+------------+---------------+---------------+----------+
|      | TOTAL      |               |               |   162.65 |
+------+------------+---------------+---------------+----------+ 
```

## Summary by category
```
+---------------+---------------+
| Category      |   Total spent |
+===============+===============+
| Food          |         91.19 |
+---------------+---------------+
| Travel        |         43.47 |
+---------------+---------------+
| Subscriptions |          9.99 |
+---------------+---------------+
| Health        |         18.00 |
+---------------+---------------+
| TOTAL         |        162.65 |
+---------------+---------------+ 
```

## Summary by month
```
+--------------+---------------+
| Month-Year   |   Total spent |
+==============+===============+
| June-2023    |        162.65 |
+--------------+---------------+
| TOTAL        |        162.65 |
+--------------+---------------+ 
```