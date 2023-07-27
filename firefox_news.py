from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from tqdm import tqdm
import requests
import time
import os






def wait_for_page_to_load(driver, timeout=10):
    try:
        # Wait until the body element is present on the page
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//body"))
        )

        print("Page has finished loading.")
    except TimeoutException:
        print("Page took too long to load.")


def headless_start_firefox(headless = False):

    if headless == True:
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        print("[0] You have opened Firefox on headless start option [1]")
    else:
        driver = webdriver.Firefox()
    
    return driver



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


def download_images(image_urls, download_path):
    os.makedirs(download_path, exist_ok=True)
    
    for i, url in tqdm(enumerate(image_urls)):
        try:
            response = requests.get(url)
            with open(os.path.join(download_path, f'image_{i}.jpg'), 'wb') as f:
                f.write(response.content)
        except:
            print(f"Failed to download image {i}")



def get_image_urls(driver):
    image_urls = []
    
    # Find all image elements
    image_elements = driver.find_elements_by_css_selector('.rg_i.Q4LuWd')
    
    for image_element in image_elements:
        try:
            # Click on the image thumbnail to open the full-size image
            image_element.click()
            time.sleep(1)
            
            # Find the full-size image element
            full_image_element = driver.find_element_by_xpath("//img[@class='n3VNCb']")
            image_url = full_image_element.get_attribute('src')
            
            # Append the image URL to the list
            if image_url and image_url.startswith('http'):
                image_urls.append(image_url)
        except:
            continue

    return image_urls



def search_messi_images(query):
    print(f"Searching the \"{query}\" on google images")
    driver = headless_start_firefox(False)

    driver.get("https://www.google.com/imghp?hl=en")
    driver.find_element(By.NAME, "q").send_keys(query)
    driver.find_element(By.NAME, "q").send_keys(Keys.ENTER)
    time.sleep(1)

    start_time = time.time()
    # Replace 'your_driver_instance' with your WebDriver instance
    wait_for_page_to_load(driver,timeout=5)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


    scroll_to_bottom(driver)
    
    image_urls = get_image_urls(driver)
    download_images(image_urls, 'downloaded_images')


def search_duck_duck_go(search_query,num_images = 10):

    print(f"Searching the \"{search_query}\" on google images")
    driver = headless_start_firefox(False)
    img_urls = []
    # searching the query
    driver.get(f'https://duckduckgo.com/?va=v&t=ha&q={search_query}&iax=images&ia=images')
    

    # # going to Images Section
    # ba = driver.find_element(By.XPATH, "//a[@class='zcm__link  js-zci-link  js-zci-link--images']")
    # ba.click()

    # getting the images URLs
    for result in driver.find_elements(By.CSS_SELECTOR, '.js-images-link')[0:0+num_images]:
        imageURL = result.get_attribute('data-id')
        img_urls.append(imageURL)

        print(f'{imageURL}\n')

    time.sleep(10)
    driver.quit()

    return img_urls


if __name__ == "__main__":
    urls = search_duck_duck_go(search_query = 'adriana lima')
    download_images(urls, 'downloaded_images')
    # search_messi_images(query="face of messi")

