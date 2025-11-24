
import sqlite3
import pandas as pd
import os

def DB_to_EXCEL_Path(db_file_path):
    """
    Connects to an SQLite database file using its full path, extracts all tables, 
    and writes each table as a separate sheet in an Excel file saved to the 
    same directory as the input file.

    Args:
        db_file_path (str): The full path to the SQLite .db file.
    """
    
    # 1. Determine the paths for the input and output files
    # os.path.split() separates the directory path and the file name
    directory, filename = os.path.split(db_file_path)
    
    # Create the output file name by replacing the extension
    base_name, _ = os.path.splitext(filename)
    output_filename = f"{base_name}.xlsx"
    
    # Construct the full output path
    output_file_path = os.path.join(directory, output_filename)

    print(f"--- Starting export for database: **{db_file_path}** ---")
    print(f"Saving output to: **{output_file_path}**")
    print("-" * 50)

    try:
        # 2. Connect to the SQLite database
        # Note: You should use raw strings (r'...') or double backslashes ('\\') 
        # when defining Windows paths in Python, but here we assume the 
        # input variable is handled correctly by the caller.
        conn = sqlite3.connect(db_file_path)

        # 3. Get a list of all table names
        table_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(table_query, conn)['name'].tolist()

        if not tables:
            print(f"❌ No tables found in '{db_file_path}'. Nothing to export.")
            return

        print(f"✅ Found {len(tables)} tables: {', '.join(tables)}")

        # 4. Create an Excel Writer object
        with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
            
            # 5. Loop through each table and write it to a sheet
            for table_name in tables:
                print(f"  -> Exporting table: **{table_name}**...")
                
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                df.to_excel(writer, sheet_name=table_name, index=False)
                
                print(f"     -> Wrote {len(df)} rows.")

        print("-" * 50)
        print(f"🎉 **SUCCESS!** All tables exported to: {os.path.abspath(output_file_path)}")
        print("-" * 50)

    except FileNotFoundError:
        print(f"❌ Error: Database file not found at '{db_file_path}'.")
    except sqlite3.OperationalError as e:
        print(f"❌ Database Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

    finally:
        if 'conn' in locals() and conn:
            conn.close()