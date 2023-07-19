from PIL import Image
import piexif
import os
from urllib.parse import quote
import pyperclip


folder_path = "/Specific/Path"
final_Text = """"""

def extract_gps_coordinates(image_path):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Extract the EXIF data
    exif_dict = piexif.load(image.info["exif"])

    # Check if GPS data is available
    if "GPS" in exif_dict:
        gps_data = exif_dict["GPS"]

        # Extract the latitude
        lat = gps_data.get(piexif.GPSIFD.GPSLatitude)
        lat_ref = gps_data.get(piexif.GPSIFD.GPSLatitudeRef)

        if lat and lat_ref:
            lat_degrees = lat[0][0] / lat[0][1]
            lat_minutes = lat[1][0] / lat[1][1]
            lat_seconds = lat[2][0] / lat[2][1]
            lat = lat_degrees + lat_minutes / 60 + lat_seconds / 3600

            if lat_ref.decode() == "S":
                lat = -lat

        # Extract the longitude
        lon = gps_data.get(piexif.GPSIFD.GPSLongitude)
        lon_ref = gps_data.get(piexif.GPSIFD.GPSLongitudeRef)

        if lon and lon_ref:
            lon_degrees = lon[0][0] / lon[0][1]
            lon_minutes = lon[1][0] / lon[1][1]
            lon_seconds = lon[2][0] / lon[2][1]
            lon = lon_degrees + lon_minutes / 60 + lon_seconds / 3600

            if lon_ref.decode() == "W":
                lon = -lon

        return lat, lon

    return None, None

#############################################################################

def format_coordinates(coordinates, file_name):
    latitude, longitude = coordinates
    
    if not latitude is None or not longitude is None:
        def decimal_to_dms(coord):
            degrees = int(coord)
            minutes = int((coord - degrees) * 60)
            seconds = round(((coord - degrees) * 60 - minutes) * 60, 1)
            return degrees, minutes, seconds

        def get_direction(coord):
            if coord >= 0:
                return "N" if coord != 0 else ""
            else:
                return "S" if coord != 0 else ""

        latitude_deg, latitude_min, latitude_sec = decimal_to_dms(latitude)
        longitude_deg, longitude_min, longitude_sec = decimal_to_dms(longitude)

        latitude_dir = get_direction(latitude)
        longitude_dir = get_direction(longitude)

        formatted_latitude = f"{latitude_deg}°{latitude_min:02}'{latitude_sec:04.1f}\"{latitude_dir}"
        formatted_longitude = f"{longitude_deg}°{longitude_min:02}'{longitude_sec:04.1f}\"{longitude_dir}"

        return quote(f"{formatted_latitude} {formatted_longitude.replace('N', 'E')}")
    else:
        location = input(f"No GPS found, please input location for {file_name}: ")

        return f"loc:{location}"

#############################################################################

def format_google_maps(gps_coords_formatted):
    if not gps_coords_formatted[0:4] == "loc:":
        return f"https://www.google.com/maps/place/{gps_coords_formatted}"
    else:
        return gps_coords_formatted[4:]

#############################################################################


# Loop through each file in the folder
for count, file_name in enumerate(sorted(os.listdir(folder_path), key=str.lower)):
    file_path = os.path.join(folder_path, file_name)
    
    if os.path.splitext(file_name)[1] == ".JPG":
        # Perform operations on the file
        print("Processing file:", file_path)
        # Code here to do something with the file

        gps_coords = extract_gps_coordinates(file_path)
        #print(gps_coords)

        gps_coords_formatted = format_coordinates(gps_coords, file_name)
        #print(gps_coords_formatted)

        gps_coords_google_maps = format_google_maps(gps_coords_formatted)
        #print(gps_coords_google_maps)

        final_Text += f"{count}. {gps_coords_google_maps} ({file_name})\n"
    else:
        print(f"File {file_name} invalid")


pyperclip.copy(final_Text)
print("Done!")