"""Create, modify, and parse dataset CSVs."""

import csv
import datetime
import json
import os
import random
import shutil

import erasmus.spectrogram

CSV_FIELDNAMES = ["idx", "label", "label_idx",
                  "audio_path", "spectrogram_path"]
SPLIT_RATIOS = {
    "train": 0.6,
    "valid": 0.2,
    "test": 0.2
}


def split_dataset(in_dataset_path, out_dataset_path,
                  spectrograms_path=None,
                  labels=None,
                  split_ratios=SPLIT_RATIOS):
    """Split dataset into training, validation, and test sets.

    This assumes that the dataset has paths to spectrograms (to do this,
    run create_spectrograms_for_dataset() and set add_spectrograms_to_dataset
    to True).

    Creates a new dataset at `out_dataset_path`.
    """
    # Read rows from dataset
    rows = read_dataset_rows(in_dataset_path)

    # Shuffle the rows
    random.shuffle(rows)

    # Get labels from dataset (if not passed in explicitly)
    if not labels:
        labels = {label for label in [row["label"] for row in rows]}
        labels = list(labels)

    # Split dataset into separate lists by label
    rows_by_label = {}
    for label in labels:
        rows_by_label[label] = [row for row in rows if row["label"] == label]

    # Use split ratios to divide the shuffled lists
    dataset_split = {
        "train": {},
        "valid": {},
        "test": []
    }
    for label, rows_for_label, in rows_by_label.items():
        num_rows = len(rows_for_label)
        train_idx = int(num_rows * split_ratios["train"])
        valid_idx = train_idx + int(num_rows * split_ratios["valid"])
        test_idx = valid_idx + int(num_rows * split_ratios["test"])

        print("train={},valid={},test={}. "
              "num_rows={}".format(train_idx, valid_idx, test_idx,
                                   num_rows))

        dataset_split["train"][label] = rows_for_label[0:train_idx]
        dataset_split["valid"][label] = rows_for_label[train_idx:valid_idx]
        dataset_split["test"].extend(rows_for_label[valid_idx:max(test_idx,
                                                                  num_rows)])
    # Write dataset in JSON format
    json_path = os.path.join(out_dataset_path, "dataset.json")
    if not os.path.exists(os.path.dirname(json_path)):
        os.makedirs(os.path.dirname(json_path))
    with open(json_path, "w") as f:
        f.write(json.dumps(dataset_split))

    # Copy files into corresponding train, valid, test directories
    # while keeping label directory category structure
    for data_category, data in dataset_split.items():
        if data_category == "test":
            # Handle test (indexing works differently)
            rows_test = data
            for i, row in enumerate(rows_test):
                row["data_category"] = data_category
                row["test_idx"] = i

                src_path = row["spectrogram_path"]
                dst_path = os.path.join(out_dataset_path,
                                        data_category,
                                        "{}.png".format(i))

                if not os.path.exists(os.path.dirname(dst_path)):
                    os.makedirs(os.path.dirname(dst_path))

                shutil.copyfile(src_path, dst_path)
                print("Copied {} to {}".format(src_path, dst_path))
        else:
            # Handle training and validation
            for label, rows_for_label in data.items():
                for i, row in enumerate(rows_for_label):
                    print("Row {}-{}-{}: {}".format(data_category, label, i,
                                                    row))
                    row["data_category"] = data_category

                    src_path = row["spectrogram_path"]
                    dst_path = os.path.join(out_dataset_path,
                                            data_category,
                                            label,
                                            os.path.basename(src_path))

                    if not os.path.exists(os.path.dirname(dst_path)):
                        os.makedirs(os.path.dirname(dst_path))

                    shutil.copyfile(src_path, dst_path)
                    print("Copied {} to {}".format(src_path, dst_path))

    # Add description
    dataset_split["description"] = {
        "in_dataset_path": in_dataset_path,
        "out_dataset_path": out_dataset_path,
        "labels": labels,
        "split_ratios": split_ratios,
        "num_rows": len(rows),
        "created_at": str(datetime.datetime.now())
    }

    # Write dataset in JSON format
    json_path = os.path.join(out_dataset_path, "dataset.json")
    if not os.path.exists(os.path.dirname(json_path)):
        os.makedirs(os.path.dirname(json_path))
    with open(json_path, "w") as f:
        f.write(json.dumps(dataset_split))

    # Write dataset into multiple CSVs (TODO)
    # trainandvalid_path = os.path.join(out_dataset_path,
    #                                   "dataset_trainandvalid.csv")
    # test_path = os.path.join(out_dataset_path, "dataset_test.csv")
    # with open(trainandvalid_path, "w") as f:
    #     writer = csv.DictWriter(CSV_FIELDNAMES)

    print("Done splitting; new dataset at {}".format(out_dataset_path))


def create_spectrograms_for_dataset(dataset_path, spectrograms_path,
                                    add_spectrograms_to_dataset=True):
    """Create spectrograms for all files in a dataset.

    Optionally, add spectrogram paths to dataset.
    """
    rows = read_dataset_rows(dataset_path)

    for i, row in enumerate(rows):
        # Construct output path
        out_filename = "{}.{}.png".format(row["label"], row["label_idx"])
        out_path = os.path.join(spectrograms_path, row["label"], out_filename)
        print("Output path: {}".format(out_path))

        # Create spectrogram
        if os.path.isfile(out_path):
            print("Spectrogram already exists @ {}; skipping".format(out_path))
        else:
            if not os.path.exists(os.path.dirname(out_path)):
                try:
                    os.makedirs(os.path.dirname(out_path))
                except OSError as e:
                    msg = e.strerror
                    print("OSError while creating dir tree! {}".format(msg))
                    continue
            erasmus.spectrogram.create_spectrogram_for_audio(row["audio_path"],
                                                             out_path)

        # Add spectrogram path to dataset
        if add_spectrograms_to_dataset:
            row["spectrogram_path"] = out_path

    # Update dataset CSV if necessary
    if add_spectrograms_to_dataset:
        write_dataset_rows(dataset_path, rows)


def write_dataset_rows(dataset_path, rows, fieldnames=CSV_FIELDNAMES):
    """Write rows to dataset CSV."""
    with open(dataset_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_dataset_rows(dataset_path):
    """Return all rows (as a list of dicts) for an existing dataset."""
    rows = []
    with open(dataset_path, "r") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return rows


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
                   "audio_path": filepath,
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
