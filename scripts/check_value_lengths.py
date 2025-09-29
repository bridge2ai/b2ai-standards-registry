import pandas as pd
import numpy as np
import json


def analyze_column_lengths(df, check_json_length=False):
    """
    Analyze the length of values in each column of a DataFrame.
    Returns max length and row number for each column.

    Args:
        df: DataFrame to analyze
        check_json_length: If True, measure JSON string length for dicts/lists instead of element count
    """
    results = {}

    for col in df.columns:
        max_length = 0
        max_row = -1

        for idx, value in enumerate(df[col]):
            # Handle lists/arrays first (before isna check)
            if isinstance(value, (list, tuple, np.ndarray)):
                if check_json_length:
                    try:
                        # Convert to JSON string and measure length
                        json_str = json.dumps(value.tolist() if isinstance(
                            value, np.ndarray) else value)
                        length = len(json_str)
                    except (TypeError, ValueError):
                        # Fallback to string representation
                        length = len(str(value))
                else:
                    length = len(value)
            # Handle dictionaries
            elif isinstance(value, dict):
                if check_json_length:
                    try:
                        json_str = json.dumps(value)
                        length = len(json_str)
                    except (TypeError, ValueError):
                        length = len(str(value))
                else:
                    length = len(value)
            # Handle NaN/None values (but not arrays)
            elif value is None or (not isinstance(value, (list, tuple, np.ndarray, dict)) and pd.isna(value)):
                length = 0
            # Handle strings
            elif isinstance(value, str):
                length = len(value)
            # Handle other types (convert to string and measure)
            else:
                length = len(str(value))

            if length > max_length:
                max_length = length
                max_row = idx

        results[col] = {
            'max_length': max_length,
            'row_number': max_row,
            'sample_value': df.iloc[max_row][col] if max_row >= 0 else None
        }

    return results


def print_length_analysis(df, check_json_length=False):
    """Print a formatted report of column length analysis."""
    results = analyze_column_lengths(df, check_json_length)

    length_type = "JSON string length" if check_json_length else "element count/character length"
    print(
        f"DataFrame Length Analysis ({len(df)} rows, {len(df.columns)} columns)")
    print(f"Measuring: {length_type}")
    print("=" * 80)

    for col, info in results.items():
        print(f"\nColumn: {col}")
        print(f"  Max Length: {info['max_length']}")
        print(f"  Row Number: {info['row_number']}")

        # Show truncated sample for very long values
        sample_repr = repr(info['sample_value'])
        if len(sample_repr) > 200:
            sample_repr = sample_repr[:197] + "..."
        print(f"  Sample Value: {sample_repr}")
        print(f"  Value Type: {type(info['sample_value']).__name__}")

        # Warn about JSON length limit
        if check_json_length and info['max_length'] > 500000:
            print(f"  ⚠️  WARNING: Exceeds typical JSON size limits!")


def find_large_json_values(df, threshold=500000):
    """Find all values that would exceed JSON size threshold."""
    large_values = []

    for col in df.columns:
        for idx, value in enumerate(df[col]):
            if isinstance(value, (list, tuple, np.ndarray, dict)):
                try:
                    json_str = json.dumps(value.tolist() if isinstance(
                        value, np.ndarray) else value)
                    if len(json_str) > threshold:
                        large_values.append({
                            'row': idx,
                            'column': col,
                            'json_length': len(json_str),
                            'value_type': type(value).__name__,
                            'preview': str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                        })
                except (TypeError, ValueError):
                    pass

    return large_values


# Example usage:
if __name__ == "__main__":
    # Create sample DataFrame with various data types
    sample_data = {
        'text': ['short', 'medium length text', 'very very long text string here'],
        'numbers': [1, 12345, 7],
        'lists': [[1, 2], [1, 2, 3, 4, 5], [7]],
        'dicts': [{'a': 1}, {'x': 1, 'y': 2, 'z': 3}, {'key': 'value'}],
        'mixed': ['text', [1, 2, 3], {'nested': 'dict'}]
    }

    df = pd.DataFrame(sample_data)
    print_length_analysis(df)

    # Check JSON string lengths (important for synapse.org)
    print("\n" + "=" * 50)
    print("Checking for large JSON values...")
    large_values = find_large_json_values(df)
    if large_values:
        print(
            f"Found {len(large_values)} values that may cause JSON size issues:")
        for item in large_values:
            print(
                f"  Row {item['row']}, Column '{item['column']}': {item['json_length']:,} characters")
    else:
        print("No problematic JSON sizes found.")

    # Also show JSON length analysis
    print("\n" + "=" * 50)
    print("JSON String Length Analysis:")
    print_length_analysis(df, check_json_length=True)
