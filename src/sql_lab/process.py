"""Read MOCK_DATA.csv, clean it, and upload it to the `mock` table in MySQL."""

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

# Step 3: map pandas dtypes (from df.dtypes) to MySQL column types
TYPE_MAPPING = {
    "int64": "BIGINT",
    "int32": "INT",
    "float64": "DOUBLE",
    "bool": "TINYINT(1)",
    "datetime64[ns]": "DATETIME",
    "datetime64[us]": "DATETIME",  # pandas 3.0 parses dates at microsecond resolution
    "object": "VARCHAR(255)",
    "string": "VARCHAR(255)",
    "str": "VARCHAR(255)",  # pandas 3.0 reports text columns as "str"
}


def read_data(filename):
    """Load a CSV file into a pandas DataFrame and return it."""
    logging.info("Reading %s", filename)
    data = pd.read_csv(filename)
    logging.info("Read %d rows and %d columns", len(data), len(data.columns))
    return data


def clean_data(data):
    """Drop rows with missing values, fix column types, and return the cleaned DataFrame."""
    # Remove any row that has a blank in any column
    cleaned = data.dropna().copy()
    logging.info("Dropped %d rows with missing values", len(data) - len(cleaned))

    # age was read as float64 only because of the blanks, so make it whole numbers again
    cleaned["age"] = cleaned["age"].astype("int64")

    # signup_date was read as text, so convert it to real dates
    cleaned["signup_date"] = pd.to_datetime(cleaned["signup_date"])

    logging.info("Cleaned data has %d rows", len(cleaned))
    return cleaned


def load_data(data, table):
    """Create `table` if it doesn't exist and insert every row of `data` (approach A)."""
    # Stop early with a clear message if the environment variables aren't set
    if not all([DBHOST, DBUSER, DBPASS, DBNAME]):
        logging.error("Set DBHOST, DBUSER, DBPASS, and DBNAME before running this script")
        return

    # Table and column names can't be %s placeholders, so they are written into the
    # SQL text here. They come from this script and the CSV header, not from user
    # input, and backticks quote them (needed anyway since `group` is a reserved word).
    # All row VALUES below still go through %s placeholders.
    columns = list(data.columns)
    column_defs = ", ".join(
        f"`{col}` {TYPE_MAPPING.get(str(data[col].dtype), 'VARCHAR(255)')}" for col in columns
    )
    create_sql = f"CREATE TABLE IF NOT EXISTS `{table}` ({column_defs}, PRIMARY KEY (`id`))"

    column_list = ", ".join(f"`{col}`" for col in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    insert_sql = f"INSERT INTO `{table}` ({column_list}) VALUES ({placeholders})"

    connection = None
    try:
        connection = mysql.connector.connect(
            host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME
        )
        cursor = connection.cursor()

        # Create the table if this is the first run
        cursor.execute(create_sql)
        logging.info("Table `%s` is ready", table)

        # Clear out rows from any earlier run so rerunning doesn't duplicate data
        cursor.execute(f"DELETE FROM `{table}`")

        # Insert one row at a time with a parameterized query
        for row in data.itertuples(index=False, name=None):
            # pandas Timestamps -> plain Python datetimes, which mysql-connector expects
            values = tuple(v.to_pydatetime() if isinstance(v, pd.Timestamp) else v for v in row)
            cursor.execute(insert_sql, values)

        connection.commit()
        logging.info("Inserted %d rows into `%s`", len(data), table)
        cursor.close()
    except mysql.connector.Error as err:
        logging.error("Database error: %s", err)
        if connection is not None and connection.is_connected():
            connection.rollback()  # undo partial inserts so the table isn't half-loaded
    finally:
        # Always close the connection, even after an error
        if connection is not None and connection.is_connected():
            connection.close()
            logging.info("Connection closed")


def main():
    """Run the pipeline: read the CSV, clean it, and load it into the mock table."""
    data = read_data("MOCK_DATA.csv")
    data = clean_data(data)
    load_data(data, "mock")


if __name__ == "__main__":
    main()
