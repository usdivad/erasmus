"""Create, or append to, a dataset.

Example usage:
    Add to dataset:
    `python create_dataset.py data/dataset.csv data/mp3s label1`

    Add to dataset and reinitialize:
    `python create_dataset.py data/dataset.csv data/mp3s label1 -reinitialize`
"""

import argparse
import sys

import erasmus.dataset

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
    success = erasmus.dataset.add_to_dataset(args.dataset_path,
                                             args.source_path,
                                             args.source_label,
                                             args.reinitialize)

    sys.exit(0 if success else 1)
