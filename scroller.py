from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

# Target website
website = "https://store.steampowered.com/search/?category1=998&genre=Free%20to%20Play"

# Set up Firefox options
options = Options()
options.add_argument("-profile")

# Modify the path to the Firefox profile in your system
options.add_argument("/home/jyo/.mozilla/firefox/iee0ubgb.default-release/")

# Add user login info

# Create a WebDriver instance
driver = webdriver.Firefox(options=options)

# Use the driver to open a website
driver.get(website)
time.sleep(3)



# Find the first link that starts with https://store.steampowered.com/app/

while True:
    time.sleep(3)
    app_links = driver.find_elements(By.XPATH, "//a[starts-with(@href, 'https://store.steampowered.com/app/')]")


    print("Processing App Links")
    for link in app_links:
        # print("Processing:", link.get_attribute('href'))
        blacklist = []
        with open('blacklist.txt', 'r') as f:
            blacklist = f.readlines()

        blacklist = [x.strip() for x in blacklist]
        blacklist = [x.replace('\n','') for x in blacklist]

        current_link = ''
        # print("Current Blacklist:", blacklist)
        current_link = link.get_attribute('href')
        current_link = current_link.split('?snr')[0]
        if current_link not in blacklist:
            break
        else:
            continue


    print("Going to:", current_link)

    driver.get(current_link)

    time.sleep(3)

    if driver.current_url.startswith("https://store.steampowered.com/agecheck/app/"):
        try:
            # Find the button with the text "View Page"
            print("Finding the View Page button")
            view_page_button = driver.find_element(By.XPATH, "//span[contains(text(), 'View Page')]")
            # Click the button
            print("Clicking the View Page button")
            driver.execute_script("arguments[0].click();", view_page_button)
            time.sleep(3)
        except:
            print("Error: Could not find the View Page button")
            with open('blacklist.txt', 'a') as f:
                f.write(driver.current_url + '\n')
            driver.get(website)
        continue

    try:
        # Find the button with the text "Add to Library"
        print("Finding the Add to Library button")
        add_to_library_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Add to Library')]")
        # Extract the onclick attribute value
        print("Extracting the onclick attribute value")
        onclick_value = add_to_library_button.get_attribute("onclick")
        # Click the button
        print("Clicking the Add to Library button")
        driver.execute_script("arguments[0].click();", add_to_library_button)
        time.sleep(3)
    except:
        print("Error: Could not find the Add to Library button")
        with open('blacklist.txt', 'a') as f:
            f.write(driver.current_url + '\n')
        driver.get(website)
        continue

    time.sleep(5)
