import requests
from tqdm import tqdm
import time
from pathlib import Path
import concurrent.futures

def download_image(i,topic, link, download_path):
    try:
        response = requests.get(link).content
        img_name = f'{topic}_image_{i}.jpg'
        path = Path(download_path, img_name)
        path.write_bytes(response.content)
    except requests.exceptions.HTTPError as e:
        print(f"Failed to download the image for {i}. Error: {e}")


if __name__ == "__main__":

    dictionary = {}
    links = []

    with open("star_wars.txt", "r") as file:
        for line in file:
            (key, value) = line.split("==")
            dictionary[key] =  value
            links.append(value)
        file.close()

    download_path = "star_wars"
    topic = "star_wars"

    t1 = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i,url in enumerate(links):
            executor.submit(download_image, i,topic, links, download_path)

    t2 = time.perf_counter()

    print(f'Finished in {t2-t1} seconds')
