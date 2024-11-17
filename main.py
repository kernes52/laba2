import argparse
import os
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO

NASA_API_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"


def get_arguments():
    parser = argparse.ArgumentParser(description="Download Mars rover photos from NASA API.")
    parser.add_argument("--earth-date", required=True, help="Earth date for the photo (format YYYYMMDD).")
    parser.add_argument("--camera", required=True, help="Camera type (e.g., RHAZ, FHAZ).")
    parser.add_argument("--key", required=True, help="NASA API key.")
    parser.add_argument("--output-dir", default="Mars_Photos", help="Directory to save downloaded photos.")
    parser.add_argument("--show", action="store_true", help="Show the images after downloading.")
    return parser.parse_args()


def download_mars_photos(earth_date, camera, api_key, output_dir, show=False):
    try:
        date = datetime.strptime(earth_date, "%Y%m%d").strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYYMMDD.")
        return

    params = {
        "earth_date": date,
        "camera": camera,
        "api_key": api_key
    }
    response = requests.get(NASA_API_URL, params=params)

    if response.status_code != 200:
        print("Failed to connect to NASA API.")
        return

    data = response.json()

    photos = data.get("photos", [])
    if not photos:
        print("No photos found for the specified date and camera.")
        return

    rover_name = photos[0]["rover"]["name"]

    os.makedirs(output_dir, exist_ok=True)

    folder_name = f"{output_dir}/{earth_date}_{rover_name}_{camera}"
    os.makedirs(folder_name, exist_ok=True)

    for i, photo in enumerate(photos):
        img_url = photo["img_src"]
        img_data = requests.get(img_url).content
        img_name = f"{folder_name}/photo_{i + 1}.jpg"

        with open(img_name, 'wb') as img_file:
            img_file.write(img_data)

        print(f"Downloaded {img_name}")

        if show:
            img = Image.open(BytesIO(img_data))
            img.show()


if __name__ == "__main__":
    args = get_arguments()
    download_mars_photos(args.earth_date, args.camera, args.key, args.output_dir, args.show)
