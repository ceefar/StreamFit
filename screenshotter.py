from webbrowser import Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image 
from selenium.webdriver.chrome.service import Service as ChromeService
import time


def take_selenium_screenshot(url:str = "https://exrx.net/WeightExercises/PectoralSternal/BBBenchPress"):
        
    ss_index = url.rfind("/")
    ssnamepath = f"images/{url[ss_index+1:]}.png" 

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(f'{url}')
    driver.find_element_by_xpath('//*[@id="ez-accept-all"]').click()

    time.sleep(3)

    driver.save_screenshot(ssnamepath) # is probably a wait until load so its chill dw

    driver.quit()

    im = Image.open(ssnamepath)
    im = im.crop( (95, 385, 490, 690) ) # previously, image was 826 pixels wide, cropping to 825 pixels wide
    im.save(ssnamepath)

    return(ssnamepath)



# PIL import pillow library (can install with "pip install pillow")

#service = Chrome(executable_path=ChromeDriverManager().install())

# import pickle
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

# driver.add_cookie({"name":"ezux_ifep_107151","value":"true"})

# options = webdriver.ChromeOptions() # options=options
# options.add_extension("adblock.crx")  #C:/Users/robfa/Downloads/StreamFit/adblock.crx

# from selenium.webdriver.support.ui import WebDriverWait
# WebDriverWait(driver, 3)
