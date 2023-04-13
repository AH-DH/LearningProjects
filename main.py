import os
import glob
import datetime
import platform
import zipfile
from pathlib import Path

def get_bugreports_today(desktop_path):
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    pattern = os.path.join(desktop_path, f"*{today_str}*bugreport.zip")
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
    bugreports_today = get_bugreports_today(desktop_path)

    if not bugreports_today:
        print("No bugreports created today were found on the desktop.")
        return

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    device_name = platform.node().replace(" ", "_")
    output_folder = os.path.join(desktop_path, f"{date_str}_{device_name}_bugreports")
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    for bugreport_path in bugreports_today:
        file_name = os.path.basename(bugreport_path)
        os.rename(bugreport_path, os.path.join(output_folder, file_name))

    zip_file_path = os.path.join(desktop_path, f"{date_str}_{device_name}_bugreports.zip")
    create_zip_folder(output_folder, zip_file_path)

    print(f"Bugreports have been compiled and zipped to {zip_file_path}")

if __name__ == "__main__":
    main()