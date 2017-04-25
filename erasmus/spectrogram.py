"""Create spectrogram (and write it to png) for a given audio file."""

import argparse
import csv
import os
import sys

import librosa
import librosa.display
import librosa.feature
import matplotlib.pyplot as plt
import numpy as np

# import dataset


DEFAULT_DURATION = 60
DEFAULT_METHOD = "stft"  # stft, cqt, mel
DEFAULT_DATA_CATEGORY = "train"  # train, valid, test


def create_spectrograms_for_dataset(dataset_path, spectrograms_path,
                                    data_category=DEFAULT_DATA_CATEGORY):
    """Create spectrograms for all files in a dataset."""
    # fieldnames = dataset.CSV_FIELDNAMES
    # print(fieldnames)
    rows = []
    with open(dataset_path, "r") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]

    for i, row in enumerate(rows):
        # Construct output path based on data category
        # TODO: Handle this somewhere else! i.e. in dataset handlers
        # out_path = ""
        # if data_category == "train" or data_category == "valid":
        #     out_filename = "{}.{}.png".format(row["label"], row["label_idx"])
        #     out_path = os.path.join(spectrograms_path, "train",
        #                             row["label"], out_filename)
        # elif data_category == "test":
        #     out_filename = "{}.png".format(i)
        #     out_path = os.path.join(spectrograms_path, "test",
        #                             out_filename)
        # else:
        #     print("ERROR: Invalid data category {}!".format(data_category))
        #     return False

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
        create_spectrogram_for_audio(row["path"], out_path)


def create_spectrogram_for_audio(in_path, out_path,
                                 duration=DEFAULT_DURATION,
                                 method=DEFAULT_METHOD):
    """Create spectrogram for a single audio file."""
    # file_prefix, file_extension = os.path.splitext(in_path)

    # Load file using librosa
    y, sr = librosa.load(in_path, duration=duration)
    print("Loaded first {} seconds of {}".format(duration, in_path))

    # Compute spectrogram
    D = np.array([])
    if method == "stft":
        D = librosa.stft(y)
    elif method == "cqt":
        D = librosa.cqt(y)
    elif method == "mel":
        D = librosa.feature.melspectrogram(y)
    print("Computed spectrogram using method {}".format(method))

    # Plot spectrogram image only (no axes/legend/whitespace)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max))
    plt.tight_layout(pad=0)
    # plt.show()

    # Save spectrogram to file
    plt.savefig(out_path)
    print("Saved spectrogram to {}".format(out_path))


def get_spectrogram_experiment():
    """Experimentation with spectrogram/plotting parameters and setup."""
    # File setup
    data_dir = "data/experiments"
    # filename = "01. Al Martino - Here in My Heart.mp3"
    filename = "02 Heard 'Em Say.mp3"
    filename_prefix = os.path.splitext(filename)[0]
    filepath = os.path.join(data_dir, filename)

    # Load file using librosa
    # Only take first `audio_dur` seconds
    audio_dur = 60
    y, sr = librosa.load(filepath, duration=audio_dur)
    print("Loaded first {} seconds of {}".format(audio_dur, filepath))

    # Compute STFT
    D = librosa.stft(y)  # Default params
    # D = librosa.stft(y, hop_length=64)
    # D_left_short = librosa.stft(y, center=False, hop_length=64)
    print("Computed STFT")

    # Plot STFT
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                             y_axis="log", x_axis="time")
    plt.title("Log-frequency power spectrogram")
    plt.colorbar(format="%+2.0f dB")
    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(data_dir,
                             "{}_stft.png".format(filename_prefix)))
    print("Saved STFT")

    # Plot STFT image only (no axes/legend/whitespace)
    plt.figure(figsize=(10, 4))
    filename_plt = "{}_stft_img.png".format(filename_prefix)
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max))
    plt.tight_layout(pad=0)
    # plt.show()
    plt.savefig(os.path.join(data_dir, filename_plt), bbox_inches=0)
    print("Saved STFT (image only)")

    # Compute CQT and plot
    plt.figure(figsize=(10, 4))
    D2 = librosa.cqt(y)  # Default params
    # D2 = librosa.cqt(y, sr=sr, hop_length=64)
    librosa.display.specshow(librosa.amplitude_to_db(D2, ref=np.max),
                             y_axis="cqt_hz", x_axis="time")
    plt.title("Constant-Q power spectrogram")
    plt.colorbar(format="%+2.0f dB")
    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(data_dir, "{}_cqt.png".format(filename_prefix)))
    print("Saved CQT")

    # Compute mel-scaled spectrogram and plot
    plt.figure(figsize=(10, 4))
    D3 = librosa.feature.melspectrogram(y=y, sr=sr)  # Default params
    librosa.display.specshow(librosa.amplitude_to_db(D3, ref=np.max),
                             y_axis="cqt_hz", x_axis="time")
    plt.title("Mel spectrogram")
    plt.colorbar(format="%+2.0f dB")
    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(data_dir, "{}_mel.png".format(filename_prefix)))
    print("Saved mel spectrogram")


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str, help="Path to dataset CSV")
    parser.add_argument("spectrograms_path", type=str,
                        help="Path to save spectrogram files to")
    args = parser.parse_args()

    create_spectrograms_for_dataset(args.dataset_path, args.spectrograms_path)

    # create_spectrograms_for_dataset("data/experiments/dataset_experiment.csv",
    #                                 "data/experiments")

    # create_spectrogram_for_audio("data/experiments/02 Heard 'Em Say.mp3",
    #                              "data/experiments/spectrogram_experiment.png")
    # get_spectrogram_experiment()

    sys.exit(0)
