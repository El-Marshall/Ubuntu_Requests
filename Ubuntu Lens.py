import requests
import os
import hashlib
from urllib.parse import urlparse
from mimetypes import guess_extension

def get_filename_from_url(url, content_type=None):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # If no filename in URL, generate one from hash
    if not filename or '.' not in filename:
        ext = guess_extension(content_type.split(';')[0]) if content_type else '.jpg'
        filename = f"image_{hashlib.md5(url.encode()).hexdigest()}{ext}"
    return filename

def is_duplicate(filepath, content):
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            existing = f.read()
            return existing == content
    return False

def fetch_image(url, folder="Fetched_Images"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Check content type
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            print(f"✗ Skipped (not an image): {url}")
            return

        filename = get_filename_from_url(url, content_type)
        filepath = os.path.join(folder, filename)

        # Avoid duplicates
        if is_duplicate(filepath, response.content):
            print(f"✓ Duplicate skipped: {filename}")
            return

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    os.makedirs("Fetched_Images", exist_ok=True)

    urls = input("Enter image URLs (comma-separated): ").split(',')

    for url in map(str.strip, urls):
        if url:
            fetch_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()