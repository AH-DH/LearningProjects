import os
import glob
import datetime
import platform
import zipfile
from pathlib import Path

def get_zip_files_today(desktop_path):
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    pattern = os.path.join(desktop_path, f"*{today_str}*.zip")
    return glob.glob(pattern)

def create_zip_folder(folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def main():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    zip_files_today = get_zip_files_today(desktop_path)

    if not zip_files_today:
        print("No .zip files created today were found on the desktop.")
        return

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    device_name = platform.node().replace(" ", "_")
    output_folder = os.path.join(desktop_path, f"{date_str}_{device_name}_zips")
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    for zip_file_path in zip_files_today:
        file_name = os.path.basename(zip_file_path)
        os.rename(zip_file_path, os.path.join(output_folder, file_name))

    zip_file_path = os.path.join(desktop_path, f"{date_str}_{device_name}_zips.zip")
    create_zip_folder(output_folder, zip_file_path)

    print(f".zip files have been compiled and zipped to {zip_file_path}")

if __name__ == "__main__":
    main()