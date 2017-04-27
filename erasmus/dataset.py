"""Create, modify, and parse dataset CSVs."""

import csv
import os

import erasmus.spectrogram

CSV_FIELDNAMES = ["idx", "label", "label_idx",
                  "audio_path", "spectrogram_path"]
SPLIT_RATIOS = {
    "train": 0.6,
    "valid": 0.2,
    "test": 0.2
}


def split_dataset(dataset_path, spectrograms_path=None):
    """Split dataset into training, validation, and test sets."""
    # rows = read_dataset_rows(dataset_path)
    pass


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
            continue
        if not os.path.exists(os.path.dirname(out_path)):
            try:
                os.makedirs(os.path.dirname(out_path))
            except OSError as e:
                print("OSError while creating dir tree! {}".format(e.strerror))
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
