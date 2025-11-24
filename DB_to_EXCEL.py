
def DB_to_EXCEL(your_database, full_export_database_name):
    import sqlite3
    import pandas as pd
    import os

    # --- Configuration ---
    DATABASE_FILE = your_database # Replace with your .db file name
    OUTPUT_FILE = full_export_database_name # The name for your new Excel file

    # --- Main Logic ---
    print(f"Starting export for database: {DATABASE_FILE}")

    try:
        # 1. Connect to the SQLite database
        conn = sqlite3.connect(DATABASE_FILE)

        # 2. Get a list of all table names in the database
        # The 'sqlite_master' table contains metadata about all tables.
        table_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(table_query, conn)['name'].tolist()

        if not tables:
            print("❌ No tables found in the database. Nothing to export.")
            conn.close()
            exit()

        print(f"✅ Found the following tables to export: {', '.join(tables)}")
        print("-" * 30)

        # 3. Create an Excel Writer object to handle multiple sheets
        # We recommend using 'xlsxwriter' for performance if you have many tables/large data.
        with pd.ExcelWriter(OUTPUT_FILE, engine='xlsxwriter') as writer:
            
            # 4. Loop through each table, read it into a DataFrame, and write it to a sheet
            for table_name in tables:
                print(f"Exporting table: **{table_name}**...")
                
                # Read all columns and rows from the current table
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                
                # Write the DataFrame to a sheet named after the table
                # index=False prevents writing the DataFrame index as a column
                df.to_excel(writer, sheet_name=table_name, index=False)
                
                print(f"   -> Wrote {len(df)} rows to sheet '{table_name}'.")

        print("-" * 30)
        print(f"💾 **SUCCESS!** All data exported to Excel file: {os.path.abspath(OUTPUT_FILE)}")

    except sqlite3.OperationalError as e:
        print(f"❌ Database Error: {e}")
        print("Please check your database file name.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

    finally:
        # Close the database connection
        if 'conn' in locals() and conn:
            conn.close()
            print("Connection closed.")