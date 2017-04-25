"""Create, modify, and parse dataset CSVs."""

import argparse
import csv
import os
import sys


CSV_FIELDNAMES = ["idx", "path", "label", "label_idx"]


def add_to_dataset(dataset_path, source_path, source_label, reinitialize):
    """Add source files to dataset."""
    # Setup
    valid_extensions = [".mp3", ".wav", ".m4a", ".flac"]
    data_idx = 0
    label_idx = 0

    # Initialize or re-initialize CSV
    if reinitialize or not os.path.isfile(dataset_path):
        initialize_dataset(dataset_path)

    # Get proper index and label index
    with open(dataset_path, "r") as f:
        reader = csv.DictReader(f)
        # next(reader)  # Don't count header row
        rows = [row for row in reader]
        print("{} rows".format(len(rows)))
        print(rows)
        data_idx = sum(1 for row in rows)
        label_idx = sum(1 for row in rows if row["label"] == source_label)
    print("data_idx={}, label_idx={}".format(data_idx, label_idx))

    # Add source files to dataset
    with open(dataset_path, "a") as f:
        writer = csv.DictWriter(f, CSV_FIELDNAMES)
        audio_files = []
        for root, dirs, files in os.walk(source_path):
            files = [filename for filename in files
                     if os.path.splitext(filename)[1] in valid_extensions]
            audio_files.extend(files)

        for i, filename in enumerate(audio_files):
            filepath = os.path.join(root, filename)
            print("{}. {}".format(i, filepath))
            row = {"idx": data_idx + i,
                   "path": filepath,
                   "label": source_label,
                   "label_idx": label_idx + i}
            writer.writerow(row)


def initialize_dataset(dataset_path):
    """Initialize (or re-initialize) a dataset with field names as header."""
    with open(dataset_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_FIELDNAMES)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str, help="Path to dataset CSV")
    parser.add_argument("source_path", type=str,
                        help="Path to source directory containing audio files")
    parser.add_argument("source_label", type=str,
                        help="Label to apply to data in the source directory")
    parser.add_argument("-reinitialize", action="store_true",
                        help="Flag for whether or not to reinitialize dataset")
    args = parser.parse_args()

    # Add to dataset
    success = add_to_dataset(args.dataset_path, args.source_path,
                             args.source_label, args.reinitialize)

    sys.exit(0 if success else 1)
