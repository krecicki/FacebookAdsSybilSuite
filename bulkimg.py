# Scrape URLs from a website for images like yarn
# Pre-Aff-ix the URL to download the GIF in the urls.txt
import os
import requests

def download_image(url, save_dir):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_name = url.split('/')[-1]
            save_path = os.path.join(save_dir, image_name)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {url}")
        else:
            print(f"Failed to download: {url} [Status Code: {response.status_code}]")
    except Exception as e:
        print(f"Error while downloading {url}: {e}")

def bulk_download_images(urls_file, save_dir):
    with open(urls_file, 'r') as f:
        urls = f.read().splitlines()
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for url in urls:
        download_image(url, save_dir)

if __name__ == "__main__":
    urls_file = "urls.txt"  # Replace with your input .txt file name
    save_directory = "gif"  # Replace with your desired save directory

    bulk_download_images(urls_file, save_directory)