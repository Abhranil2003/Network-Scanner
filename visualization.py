from tabulate import tabulate # type: ignore

def display_table(data):
    """
    Displays the data in a tabular format using the tabulate library.

    Args:
        data (list): A list of dictionaries containing scan results.
    """
    if not data:
        print("No data to display.")
        return

    # Prepare headers from keys of the first dictionary
    headers = data[0].keys()
    
    # Prepare rows from the values of each dictionary
    rows = [list(entry.values()) for entry in data]
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))
