import os
import time
import requests
from selenium import webdriver


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1): #function definition of image fetch url it will fetch the url of the image
    def scroll_to_end(wd): #this fucntion trying to scroll the page on automated mode without us being manually doing scroll this step is required to download more images
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions) #waiting for sometime the procedure can happen

        # build the google query

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q=dog&oq=dog&gs_l=img
    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set() #url are unique and can be stored in set
    image_count = 0 #count of image
    results_start = 0
    while image_count < max_links_to_fetch: #untill image count is 5 it will run
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd") #in images i need to find Q4luWd
        number_results = len(thumbnail_results)


        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]: #now we have all the urls with Q4LuWd in form of a list we will iterate over this to make click so that we can get the link and thereafter we can fetch the actual image
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click() #clicking it
                time.sleep(sleep_between_interactions) #little time to load
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb') #it will search for this tag value to get the link of actual image
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src')) #if the value is valid one having http then it will add it to set() of image urls discussed above

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch: #if count is 5 that is image is 5 in no. as we want only 5 images we can print and break and return urls
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path:str,url:str, counter): #this fucntion is saving the iamge for me on local drive that all
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=10): #definition of function
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' '))) #target folder structuring using os library

    if not os.path.exists(target_folder): # cheching if named target folder is present or not if not create the folder
        os.makedirs(target_folder) #creation of folder

    with webdriver.Chrome(executable_path=driver_path) as wd: # with this we are able to interact with our chrome browser or open empty browser
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5) #trying to return the url of the images

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1

# pip install -r requirements.txt

# My chrome Version 85.0.4183.102
# My Firefox Version 80.0.1 (64-bit)

# How to execute this code
# Step 1 : pip install selenium, pillow, requests
# Step 2 : make sure you have chrome/Mozilla installed on your machine
# Step 3 : Check your chrome version ( go to three dot then help then about google chrome )
# Step 4 : Download the same chrome driver from here  " https://chromedriver.storage.googleapis.com/index.html "
# Step 5 : put it inside the same folder of this code


DRIVER_PATH = './chromedriver.exe'
search_term = 'Iron Man'
# num of images you can pass it from here  by default it's 10 if you are not passing
number_images = 5
search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images = number_images) #code start from here enter into the fucntion first