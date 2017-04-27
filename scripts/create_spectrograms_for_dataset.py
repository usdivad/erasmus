r"""Create spectrograms for all audio files in a dataset.

Example usage:
    `python create_spectrograms_for_dataset.py \
     data/experiments/dataset.csv \
     data/experiments/spectrograms`

"""

import argparse
import sys

import erasmus.dataset


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str, help="Path to dataset CSV")
    parser.add_argument("spectrograms_path", type=str,
                        help="Path to save spectrogram files to")
    parser.add_argument("-update_dataset", action="store_true",
                        help="Flag for whether or not to update the dataset"
                             "with spectrogram paths")
    args = parser.parse_args()

    erasmus.dataset.create_spectrograms_for_dataset(args.dataset_path,
                                                    args.spectrograms_path,
                                                    args.update_dataset)

    sys.exit(0)
