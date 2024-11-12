import time
import sys
import logging
from logging.handlers import RotatingFileHandler
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import os
import pickle
import urllib.parse
from requests.auth import HTTPBasicAuth

# Retrieve tokens from file
def retrieve_tokens():
    try:
        with open('tokens.pkl', 'rb') as file:
            tokens = pickle.load(file)
            return tokens
    except FileNotFoundError:
        print("Token file not found. Please authenticate first.")
        return None

# Spotify API credentials
client_id = 'INSERT YOUR CLIENT ID'
client_secret = 'INSERT YOUR CLIENT SECRET'

def get_spotify_access_token():
    tokens = retrieve_tokens()
    if not tokens:
        raise Exception("Re-authentication required. Tokens not found.")

    refresh_token = tokens.get('refresh_token')
    if not refresh_token:
        print("Refresh token is missing. Please re-authenticate.")
        raise Exception("Re-authentication required due to missing refresh token.")

    url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    auth = HTTPBasicAuth(client_id, client_secret)

    response = requests.post(url, headers=headers, data=payload, auth=auth)
    response_data = response.json()

    if response.status_code == 200:
        access_token = response_data['access_token']
        new_refresh_token = response_data.get('refresh_token', refresh_token)
        store_tokens(access_token, new_refresh_token)  # Store both tokens
        return access_token
    else:
        raise Exception(
            f"Error fetching access token: {response_data.get('error_description', 'Unknown error')}"
        )

def store_tokens(access_token, refresh_token):
    tokens = {'access_token': access_token, 'refresh_token': refresh_token}
    with open('tokens.pkl', 'wb') as file:
        pickle.dump(tokens, file)

def get_current_song_image():
    tokens = retrieve_tokens()
    if not tokens:
        return None

    access_token = tokens.get('access_token')
    url = 'https://api.spotify.com/v1/me/player/currently-playing'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'item' in data and 'album' in data['item'] and 'images' in data['item']['album']:
            images = data['item']['album']['images']
            if images:
                return images[0]['url']
        return None
    elif response.status_code == 401:
        print("Access token expired, refreshing token...")
        try:
            access_token = get_spotify_access_token()
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if 'item' in data and 'album' in data['item'] and 'images' in data['item']['album']:
                    images = data['item']['album']['images']
                    if images:
                        return images[0]['url']
                return None
            else:
                return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
    else:
        return None

def display_image():
    default_image_path = 'INSERT_YOUR_IMAGE.png'
    if not os.path.exists(default_image_path):
        print("Fallback image not found. Please add 'fallback_image.png' in the directory.")
        sys.exit(1)

    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='spotipy.log',
                        level=logging.INFO)
    logger = logging.getLogger('spotipy_logger')

    handler = RotatingFileHandler('spotipy.log', maxBytes=2000, backupCount=3)
    logger.addHandler(handler)

    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat-pwm'
    options.gpio_slowdown = 2
    options.brightness = 70
    options.limit_refresh_rate_hz = 60

    matrix = RGBMatrix(options=options)

    try:
        while True:
            try:
                imageURL = get_current_song_image()
                if imageURL:
                    response = requests.get(imageURL)
                    try:
                        image = Image.open(BytesIO(response.content))
                        image.thumbnail((matrix.width, matrix.height), Image.Resampling.LANCZOS)
                        matrix.SetImage(image.convert('RGB'))
                    except UnidentifiedImageError:
                        print("Failed to identify the image file, loading fallback image.")
                        image = Image.open(default_image_path)
                        image.thumbnail((matrix.width, matrix.height), Image.Resampling.LANCZOS)
                        matrix.SetImage(image.convert('RGB'))
                else:
                    print("No valid image URL found, loading fallback image.")
                    image = Image.open(default_image_path)
                    image.thumbnail((matrix.width, matrix.height), Image.Resampling.LANCZOS)
                    matrix.SetImage(image.convert('RGB'))

                time.sleep(5)
            except Exception as e:
                print(f"Error occurred: {e}")
                image = Image.open(default_image_path)
                image.thumbnail((matrix.width, matrix.height), Image.Resampling.LANCZOS)
                matrix.SetImage(image.convert('RGB'))
                time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)

def main():
    display_image()

if __name__ == '__main__':
    main()
