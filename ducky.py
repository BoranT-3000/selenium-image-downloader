import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from tqdm import tqdm
import requests

#this will click every image 
# document.getElementsByClassName('tile  tile--img  has-detail')[3].click()

# this will get the length of images 
# document.getElementsByClassName('tile  tile--img  has-detail').length 

# this will get image inside that div 
"document.querySelector('div.detail__media__img-wrapper a').getAttribute('href'); "

# this will give you the title of that image inside that website
# document.getElementsByClassName('detail__body  detail__body--images')[1].children[0].children[0].innerText 


def headless_start_firefox(headless = False):

    if headless == True:
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        print("[0] You have opened Firefox on headless start option [1]")
    else:
        driver = webdriver.Firefox()
        print("[0] Firefox is starting, You have opened Firefox [1]")
    
    return driver

def create_directory(dir_name):
    # to get the current working directory
    directory = os.getcwd()
    complete_path = os.path.join(directory, dir_name)
    try:
        os.makedirs(complete_path, exist_ok=True)
        print("The new directory is created!")
        return True, complete_path
    except OSError as e:
        if e.errno == 17:  # Error number 17 is 'FileExistsError', which means the directory already exists.
            print("You already have such a directory.")
            return False, complete_path
        else:
            print(f"An error occurred: {e}")
            return False, complete_path

def scroll_to_bottom(driver):
    # Store the starting position
    start_height = driver.execute_script('return document.body.scrollTop || document.documentElement.scrollTop || window.pageYOffset || 0')

    i = 0 
    while True:
        i = i +1 
        print(f'scrolling down [{i}] times')
        
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        
        # Waiting for the results to load
        # Increase the sleep time if your internet is slow
        time.sleep(3)
        
        new_height = driver.execute_script('return document.body.scrollHeight')

        time.sleep(3)
        # If no button is found, check if new images have been loaded
        if new_height > start_height:
            start_height = new_height
        else:
            # If no new images are loaded, scroll back to the starting position
            print('[Going Up] sorry there are no more images to be found')
            driver.execute_script(f'window.scrollTo(0, {0});')
            break


def download_images(topic,image_urls, download_path):
    
    for i, (title, url) in tqdm(enumerate(image_urls.items())):
        try:
            response = requests.get(url, stream=True)
            if 'data:' not in url and response.status_code == 200:
                with open(os.path.join(download_path, f'{topic}_image_{i}.jpg'), 'wb') as f:
                    f.write(response.content)
                # print("Image downloaded successfully.")
                # print(f"[INFO] --> Success {f}")
            elif 'data:' in url:
                print(f"Skipping download for {title}. The URL contains 'data:'.")
            else:
                print(f"Failed to download the image for {title}.")
        except:
            print(f"Failed to download image for {title}")

# Function to add a new title and URL to the dictionary
def add_title_and_url(title, url):
    title_url_dict[title] = url

search_query = "Star Wars"
transformed_name = search_query.lower().replace(" ", "_")
is_created, path = create_directory(dir_name=transformed_name)
print(f"Directory created: {is_created}, Complete path: {path}")
driver = headless_start_firefox(False)

url = f"https://duckduckgo.com/?va=r&t=he&q={search_query}&iax=images&ia=images"
driver.get(url)

scroll_to_bottom(driver)

time.sleep(2)

count_of_images = driver.execute_script('return document.getElementsByClassName("tile  tile--img  has-detail").length')
print(f"Count of all the images inside the search is : {count_of_images}")


# Initialize an empty dictionary to store titles and URLs
title_url_dict = {}

# list_of_titles, list_of_links = list(), list()
i = 0 

try :
    while i<count_of_images:
        
        driver.execute_script(f'document.getElementsByClassName("tile  tile--img  has-detail")[{i}].click()')
        time.sleep(1)

        title = driver.execute_script('return document.getElementsByClassName("detail__body  detail__body--images")[1].children[0].children[0].innerText')
        link = driver.execute_script('return document.querySelector("div.detail__media__img-wrapper a").getAttribute("href")')
        
        # list_of_titles.append(title)
        # list_of_links.append(link)
        add_title_and_url(title, link)
        

        print(f'{title}\n{link}\n')

        i=i+1
except:
    print("Not worked")

driver.quit()

# # Displaying the current dictionary
# print(title_url_dict)

# Save the dictionary to a file
file_path = f"{transformed_name}.txt"
with open(file_path, "w", encoding="utf-8") as f:
    for title, url in title_url_dict.items():
        f.write('%s:%s\n' % (title, url))

print("Data saved to:", file_path)


download_images(transformed_name,link,path)









