"""Create, modify, and parse dataset CSVs."""

import csv
import os


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
            filepaths = [os.path.join(root, filename) for filename in files
                         if os.path.splitext(filename)[1] in valid_extensions]
            audio_files.extend(filepaths)

        for i, filepath in enumerate(audio_files):
            print("{}. {}".format(i, filepath))
            row = {"idx": data_idx + i,
                   "path": filepath,
                   "label": source_label,
                   "label_idx": label_idx + i}
            writer.writerow(row)


def initialize_dataset(dataset_path):
    """Initialize (or re-initialize) a dataset with field names as header."""
    if not os.path.exists(os.path.dirname(dataset_path)):
        try:
            os.makedirs(os.path.dirname(dataset_path))
        except OSError as e:
            print("OSError while creating dir tree! {}".format(e.strerror))

    with open(dataset_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_FIELDNAMES)
