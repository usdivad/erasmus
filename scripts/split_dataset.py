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
    parser.add_argument("-labels", nargs="+", required=False,
                        help="Custom list of labels")
    args = parser.parse_args()

    if args.labels is not None:
        erasmus.dataset.split_dataset(args.in_dataset_path,
                                      args.out_dataset_path,
                                      labels=args.labels)
    else:
        erasmus.dataset.split_dataset(args.in_dataset_path,
                                      args.out_dataset_path)

    sys.exit(0)
