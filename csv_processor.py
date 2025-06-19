import argparse
import csv
from tabulate import tabulate
from typing import List, Dict, Union, Optional, Callable


def read_csv(file_path: str) -> List[Dict[str, Union[str, float]]]:
    """Read CSV file and return a list of dictionaries."""
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def filter_data(
    data: List[Dict[str, Union[str, float]]],
    column: str,
    operator: str,
    value: str
) -> List[Dict[str, Union[str, float]]]:
    """Filter data based on column, operator, and value."""
    filtered_data = []
    for row in data:
        row_value = row[column]
        try:
            # Try to convert to float for numeric comparison
            row_value_float = float(row_value)
            value_float = float(value)
            if operator == '>' and row_value_float > value_float:
                filtered_data.append(row)
            elif operator == '<' and row_value_float < value_float:
                filtered_data.append(row)
            elif operator == '==' and row_value_float == value_float:
                filtered_data.append(row)
        except ValueError:
            # Fall back to string comparison
            if operator == '==' and row_value == value:
                filtered_data.append(row)
    return filtered_data


def aggregate_data(
    data: List[Dict[str, Union[str, float]]],
    column: str,
    operation: str
) -> Optional[float]:
    """Aggregate data based on column and operation."""
    values = []
    for row in data:
        try:
            value = float(row[column])
            values.append(value)
        except ValueError:
            return None

    if not values:
        return None

    if operation == 'avg':
        return sum(values) / len(values)
    elif operation == 'min':
        return min(values)
    elif operation == 'max':
        return max(values)
    else:
        return None


def main():
    parser = argparse.ArgumentParser(description='Process CSV file.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file')
    
    # Filter arguments
    parser.add_argument('--filter', type=str, 
                        help='Filter condition in format "column,operator,value" (e.g., "price,>,100")')
    
    # Aggregate arguments
    parser.add_argument('--aggregate', type=str, 
                        help='Aggregate condition in format "column,operation" (e.g., "price,avg")')

    args = parser.parse_args()

    data = read_csv(args.file_path)

    if args.filter:
        try:
            column, operator, value = args.filter.split(',')
            data = filter_data(data, column, operator, value)
        except ValueError:
            print("Invalid filter format. Use 'column,operator,value'")
            return

    if args.aggregate:
        try:
            column, operation = args.aggregate.split(',')
            result = aggregate_data(data, column, operation)
            if result is not None:
                print(f"{operation}({column}) = {result:.2f}" if operation == 'avg' else f"{operation}({column}) = {result}")
            else:
                print(f"Cannot perform {operation} on non-numeric column '{column}'")
        except ValueError:
            print("Invalid aggregate format. Use 'column,operation'")
        return

    # Display filtered data if no aggregation
    if data:
        print(tabulate(data, headers="keys", tablefmt="grid"))
    else:
        print("No data matching the filter criteria.")


if __name__ == '__main__':
    main()
