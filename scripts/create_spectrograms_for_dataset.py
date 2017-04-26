r"""Create spectrograms for all files in a dataset.

Example usage:
    `python create_spectrograms_for_dataset.py \
     data/experiments/dataset.csv \
     data/experiments/spectrograms`

"""

import argparse
import os
import sys

import erasmus.dataset
import erasmus.spectrogram


def create_spectrograms_for_dataset(dataset_path, spectrograms_path):
    """Create spectrograms for all files in a dataset."""
    rows = erasmus.dataset.get_dataset_rows(dataset_path)

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
        erasmus.spectrogram.create_spectrogram_for_audio(row["path"], out_path)

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str, help="Path to dataset CSV")
    parser.add_argument("spectrograms_path", type=str,
                        help="Path to save spectrogram files to")
    args = parser.parse_args()

    create_spectrograms_for_dataset(args.dataset_path, args.spectrograms_path)

    sys.exit(0)
