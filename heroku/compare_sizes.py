import os
import argparse

def compare_sizes(original_file, converted_file):
    original_size = os.path.getsize(original_file)
    converted_size = os.path.getsize(converted_file)

    print(f"Original file: {original_file}")
    print(f"Converted file: {converted_file}")
    print(f"Original size: {original_size} bytes")
    print(f"Converted size: {converted_size} bytes")
    reduction = (1 - converted_size / original_size) * 100
    print(f"Size reduction: {reduction:.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare the sizes of an original PNG file and a VIC file.")
    parser.add_argument("original_file", help="Path to the original PNG file.")
    parser.add_argument("converted_file", help="Path to the converted VIC file.")
    args = parser.parse_args()

    compare_sizes(args.original_file, args.converted_file)
