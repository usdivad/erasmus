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
    args = parser.parse_args()

    erasmus.dataset.create_spectrograms_for_dataset(args.dataset_path,
                                                    args.spectrograms_path)

    sys.exit(0)
