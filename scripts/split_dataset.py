r"""Split dataset into training, validation, and test sets.

Example usage:
    `python split_dataset.py \
     data/experiments/dataset1.csv \
     data/experiments/dataset1_split_0`

"""

import argparse
import sys

import erasmus.dataset


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("in_dataset_path", type=str,
                        help="Path to input dataset CSV")
    parser.add_argument("out_dataset_path", type=str,
                        help="Path to write new dataset to (with files)")
    args = parser.parse_args()

    erasmus.dataset.split_dataset(args.in_dataset_path, args.out_dataset_path)

    sys.exit(0)
