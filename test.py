# Import the libraries.
import requests
import time
import os
import urllib
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from concurrent.futures import ThreadPoolExecutor



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

def headless_start_firefox(headless = False):

    if headless == True:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Firefox(options=options)
        print("[0] You have opened Firefox on headless start option [1]")
    else:
        driver = webdriver.Firefox()
    
    return driver

def download_images(image_urls, download_path):
    for i, url in tqdm(enumerate(image_urls)):
        try:
            
            response = requests.get(url,stream=True)
            if 'data:' not in url and response.status_code == 200:
                with open(os.path.join(download_path, f'image_{i}.jpg'), 'wb') as f:
                    f.write(response.content)
                    f.close()
                    # print("Image downloaded successfully.")
                    # print(f"[INFO] --> Success {f}")
            elif 'data:' in url:
                print("Skipping download. The URL contains 'data:'.")
            else:
                print("Failed to download the image.")
        except:
            print(f"Failed to download image {i}")

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

        # Check if the "Show more results" button exists and click it
        button = driver.find_element(By.CSS_SELECTOR, "input.LZ4I")
        if button.is_displayed():
            button.click()
            # Waiting for the results to load
            # Increase the sleep time if your internet is slow
            time.sleep(3)
        else:
            # If no button is found, check if new images have been loaded
            if new_height > start_height:
                start_height = new_height
            else:
                # If no new images are loaded, scroll back to the starting position
                print('[Going Up] sorry there are no more images to be found')
                driver.execute_script(f'window.scrollTo(0, {0});')
                break
    

    length_of_content = driver.execute_script(
        'return document.getElementsByClassName("isv-r PNCib MSM1fd BUooTd").length'
    )
    return length_of_content

def download_google_images(search_query, num_images=10,image_type='s'):

    print(f"Searching the \"{search_query}\" on google images")

    # Create the URL for a Google image search.
    url = f"https://www.google.com/search?q={search_query}&tbm=isch&tbs=sur%3Afc&hl=en&ved=0CAIQpwVqFwoTCKCa1c6s4-oCFQAAAAAdAAAAABAC&biw=1251&bih=568"
    
    
    transformed_name = search_query.lower().replace(" ", "_")

    is_created, path = create_directory(dir_name=transformed_name)
    print(f"Directory created: {is_created}, Complete path: {path}")

    # Launch the browser and open the given URL in the webdriver.
    driver = headless_start_firefox(False)
    driver.get(url)
    
    print("Google images is opened now [search is starting]")
    
    # Scroll down the body of the web page to load more images.
    length_of_content = scroll_to_bottom(driver)  
    
      
    if image_type == 's' or image_type == 'S':
        # Find the image elements.
        imgResults = driver.find_elements(By.XPATH, "//img[contains(@class,'Q4LuWd')]")
    
        # Access and store the src list of image URLs.
        src = []
        for img in imgResults:
            src.append(img.get_attribute('src'))
    
        print(f"Length of the found images is {len(src)}")

        # Retrieve and download the images.
        for i in tqdm(range(min(num_images, len(src)))):
            urllib.request.urlretrieve(str(src[i]), f"{path}/{transformed_name}{i}.jpg")

    elif image_type == 'b' or image_type == 'B':
        
        length_of_content = driver.execute_script(
        'return document.getElementsByClassName("isv-r PNCib MSM1fd BUooTd").length'
        )

        print(f"[INFO] --> {search_query.upper()} has {length_of_content} items")

        img_url_set = set()


        for i in tqdm(range(1, length_of_content)):
            try:

                driver.execute_script(
                    f'document.getElementsByClassName("bRMDJf islir")[{i}].click()'
                )

                img_href_src0 = driver.execute_script(
                    'return document.getElementsByClassName("r48jcc")[0].src '
                )
                img_url_set.add(img_href_src0)


            except Exception as e:
                print(f"[INFO] ERROR - {e}")
                print(
                    "Couldn't download an image %s, continuing downloading the next one"
                    % (i)
                )
                print("could not clicked sorry")
        
            # Use set comprehension to filter out elements containing "data:" and only show the remaining strings
            filtered_letters = [letter for letter in img_url_set if "data:" not in letter]

            with ThreadPoolExecutor(max_workers=8) as executor:
                executor.map(download_images, filtered_letters,path) 

    # Close the browser window.
    driver.quit()

if __name__ == "__main__":
    # Call the function to download 10 images of pets (change the search_query and num_images as needed).
    download_google_images(search_query='Ronaldo', num_images=10,image_type='b')