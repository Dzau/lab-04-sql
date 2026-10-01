"""Query the `mock` table in the COMPUTING_ID_mock database."""

import logging
import os

import mysql.connector
import pandas as pd

# Show timestamped status messages in the terminal
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Database credentials come from environment variables, never from the code itself
DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")
DBNAME = os.environ.get("DBNAME")

# Columns in the mock table; plot_counts only accepts names from this list
MOCK_COLUMNS = ("id", "group", "first_name", "age", "score", "signup_date")


def run_query(sql, params=()):
    """Run a SELECT with optional %s parameters and return the results as a DataFrame."""
    # Stop early with a clear message if the environment variables aren't set
    if not all([DBHOST, DBUSER, DBPASS, DBNAME]):
        logging.error("Set DBHOST, DBUSER, DBPASS, and DBNAME before running this script")
        return pd.DataFrame()

    connection = None
    try:
        connection = mysql.connector.connect(
            host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME
        )
        cursor = connection.cursor()
        # Values are passed separately as a tuple, so the library escapes them safely
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        result = pd.DataFrame(rows, columns=cursor.column_names)
        cursor.close()
        logging.info("Query returned %d rows", len(result))
        return result
    except mysql.connector.Error as err:
        logging.error("Database error: %s", err)
        return pd.DataFrame()
    finally:
        # Always close the connection, even after an error
        if connection is not None and connection.is_connected():
            connection.close()


def get_data_by_group(value):
    """Return all rows from `mock` where the `group` column equals `value`.

    Filter column: `group` (backticked in the SQL because GROUP is a reserved word).
    """
    logging.info("Getting rows where group = %s", value)
    sql = "SELECT * FROM mock WHERE `group` = %s"
    return run_query(sql, (value,))  # one-item tuple needs the trailing comma


def plot_counts(groupby):
    """Return the number of rows in `mock` for each distinct value of column `groupby`."""
    # Column names can't be %s placeholders, so only accept known column names.
    # This stops anything else from being written into the SQL text.
    if groupby not in MOCK_COLUMNS:
        logging.error("Unknown column %s; choose from %s", groupby, MOCK_COLUMNS)
        return pd.DataFrame()

    logging.info("Counting rows per %s", groupby)
    sql = f"SELECT `{groupby}`, COUNT(*) AS count FROM mock GROUP BY `{groupby}` ORDER BY count DESC"
    return run_query(sql)


def main():
    """Demonstrate the query functions on the mock table."""
    print("Rows where group = 'blue':")
    print(get_data_by_group("blue"))

    print("\nRow counts per group:")
    print(plot_counts("group"))


if __name__ == "__main__":
    main()
