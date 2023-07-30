from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from PIL import Image
import requests, time, io, os
from datetime import datetime

directory = os.getcwd()

PATH = r"chromedriver.exe"


def headless_start(mode=True):
    options = Options()
    options.headless = mode
    return webdriver.Chrome(options=options)


def create_dir(path):
    complete_path = f"{directory}\\" + path
    isExist = os.path.exists(complete_path)
    if not isExist:
        os.makedirs(complete_path)
        print("The new directory is created!")
    else:
        print("you already have such a directory")
    return complete_path


def file_log(file_name, text):
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")

    file_list = os.listdir()

    file_list_set = set(file_list)
    if f"{file_name}.txt" in file_list_set:
        operation_code = "a"
    else:
        operation_code = "w"

    file = open(f"{file_name}.txt", operation_code, encoding="utf-8")
    file.write(f"[{now}] [{text}]\n")
    file.close()


def download_image(download_path, url, image_name, title, i):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        # file_path = download_path + image_name

        with open(os.path.join(download_path, image_name), "wb") as file:
            image.save(file, "JPEG")
        # print(f"SUCCESS] [{i}]- saved {url} - as {image_name}")
        file_log(title, f"[SUCCESS] [URL] [{i}] {url} - as {image_name}")
    except Exception as e:
        # print(f"[ERROR] [{i}]- Could not save {url} - {e}")
        file_log(title, f"[ERROR] [{i}]- Could not save {url} - {e}")


def yandex_scrool():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        try:
            show_more = driver.execute_script(
                'return document.getElementsByClassName("button2__text")[2].innerText'
            )
            if "Daha fazla görsel" in show_more:
                print("We Have more results than we think")
                driver.find_element_by_xpath(
                    "/html/body/div[3]/div[2]/div[1]/div[2]/a"
                ).click()
                driver.execute_script(
                    "document.getElementsByClassName('button2 button2_size_l button2_theme_action button2_type_link button2_view_classic more__button i-bem button2_js_inited')[0].click()"
                )
            time.sleep(2)
        except:
            pass
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    length_of_content = driver.execute_script(
        'return document.getElementsByClassName("serp-item__thumb justifier__thumb").length'
    )

    driver.execute_script("window.scrollTo(0, 0);")

    return length_of_content


def print_progressbar(total, current, barsize=60):
    progress = int(current * barsize / total)
    completed = str(int(current * 100 / total)) + "%"
    print(
        "[",
        "#" * progress,
        " ",
        completed,
        "." * (barsize - progress),
        "] ",
        str(current) + "/" + str(total),
        sep="",
        end="\r",
        flush=True,
    )


driver = headless_start(False)


def main(title):

    # title = input("enter the title: ")
    dir_name = create_dir(title)
    file_log(title, f"{title}.txt is created")
    time.sleep(1)
    url = r"https://yandex.com.tr/gorsel/"
    driver.get(url)

    searchInput = driver.find_elements_by_name("text")[0]
    time.sleep(1)
    searchInput.send_keys(title)
    time.sleep(1)
    searchInput.send_keys(Keys.ENTER)
    time.sleep(3)

    num_of_img = yandex_scrool()
    print(f"[INFO] --> {title.upper()} has {num_of_img} items")
    file_log(title, f"[INFO] --> {title.upper()} has {num_of_img} items")

    print_frequency = max(min(num_of_img // 60, 100), 1)
    print("Start Task..", flush=True)
    for i in range(0, num_of_img):
        image_url = driver.execute_script(
            f'return document.getElementsByClassName("serp-item__thumb justifier__thumb")[{i}].src'
        )

        download_image(
            dir_name, image_url, f"{dir_name}\{title}_{str(i)}.png", title, i
        )

        if i % print_frequency == 0 or i == 1:
            print_progressbar(num_of_img, i, 60)

        # print(f"[URL] [{i}] [{image_url}]")

        file_log(title, f"[URL] [{i}] [{image_url}]")

    print("\nFinished", flush=True)

    time.sleep(3)


if __name__ == "__main__":

    with open("topics.txt", "r", encoding="utf-8") as f:
        topic_list = [line.strip() for line in f]

    print(topic_list)

    for title in topic_list:
        main(title)

    driver.close()
