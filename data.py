from euros import download_latest_euro_draw_file, drawn_euro_numbers
from lotto import download_latest_lotto_draw_file, drawn_lotto_numbers


def main():

    # Step 1: Download the latest draw files from National Lottery website
    if download_latest_euro_draw_file() and download_latest_lotto_draw_file():
        print("Downloaded latest draw files from National Lottery website")
    else:
        print("Could not download latest draw files")
        return

    # Step 2: Read the drawn numbers from the downloaded files
    if drawn_euro_numbers() and drawn_lotto_numbers():
        print("Read the drawn numbers from the downloaded files")
    else:
        print("Could not read the drawn numbers")
        return


if __name__ == "__main__":
    main()
