#!/bin/env python3

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import urllib.request
import subprocess
import time
from datetime import datetime

# var
# print("var")
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
logfile_name = __file__ + ".log"

"""
def download_images(driver, start_number=1):
    print('execute def download_images')
    img_tags = driver.find_element(By.TAG_NAME, "img")
    for idx, img in enumerate(img_tags, start=start_number):
        img_url = img.get_attribute("src")
        filename = f"{idx:04}.avif"
        # filename = f"{idx:04}.webp"
        urllib.request.urlretrieve(img_url, filename)
    return idx + 1
"""

def download_images(driver, pg_url, start_number=1):
    img_tag = driver.find_element(By.CLASS_NAME, "lillie") # img/source
    img_url = img_tag.get_attribute("src") #src/srcset
    filename = f"{start_number:04}.webp"
    tries=str(2)
    timeout=str(5)
    subprocess.call(['wget', '-c', '-nc', '--tries=' + tries, '--timeout=' + timeout, '-O', filename, "--referer=" + pg_url, "--user-agent=" + ua, img_url])
    """
    req = urllib.request.Request(img_url)
    req.add_header('Referer', pg_url)
    req.add_header('User-Agent', ua)
    with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
        data = response.read()
        out_file.write(data)
    """
    return start_number + 1


def main():
    # print("main")
    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=' + ua)
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)


    # Process input lines
    # print("Process input lines")
    previous_dir = os.getcwd()
    while True:
        try:
            line = input()
        except EOFError:
            break

        # Check if input is URL
        # print("Check if input is URL")
        if line.startswith("http"):
            # print("true")
            driver.get(line)
            # print("driver got")
        else:
            # print("false")
            os.chdir(previous_dir)
            title_dir = line.replace(" ", "_")
            # Log(Download Start)
            nowdate = datetime.now()
            formatted_nowdate = nowdate.strftime("%Y%m%d_%H%M%S")
            logmessage = formatted_nowdate + " \"" + title_dir + "\" is created."
            print(logmessage)
            with open(logfile_name, "a") as f:
                print(logmessage, file=f)

            os.makedirs(title_dir, exist_ok=True)
            os.chdir(title_dir)
            continue


        # Create pg_url from the first <li> <div> <a>
        # print("Create pg_url from the first <li> <div> <a>")
        href = driver.find_element(By.CSS_SELECTOR, 'ul.thumbnail-list li div a').get_attribute("href")
        page_num = 1
        img_pg_url_base = href.split('#')[0]
        img_pg_url_base += "#"

        # Create directory from text within <a> tag
        # print("Create directory from text within <a> tag")
        a_text = driver.find_element(By.CSS_SELECTOR, '#gallery-brand a').text.replace(" ", "_")
        page_id = line.split('-')[-1].split('#')[0].replace(".html", "")
        gen_dir  = page_id + "_" + a_text
        # Log(Download Start)
        nowdate = datetime.now()
        formatted_nowdate = nowdate.strftime("%Y%m%d_%H%M%S")
        logmessage = formatted_nowdate + " \"" + gen_dir + "\" is download started!"
        print(logmessage)
        with open(logfile_name, "a") as f:
            print(logmessage, file=f)

        os.makedirs(gen_dir, exist_ok=True)
        os.chdir(gen_dir)


        start_number = 1
        while True:
            # Navigate to next page
            # print("Navigate to next page")
            img_pg_url = img_pg_url_base + str(page_num)
            driver.get(img_pg_url)

            # Download images
            # print("Download images")
            start_number = download_images(driver, line, start_number)

            # Check class of the second <li> in <ul class="nav navbar-nav">
            li_class = driver.find_element(By.CSS_SELECTOR, 'ul.nav.navbar-nav li:nth-child(1)').get_attribute("class")
            if li_class == "disabled":
                break

            page_num += 1


        # Log(Downloaded)
        nowdate = datetime.now()
        formatted_nowdate = nowdate.strftime("%Y%m%d_%H%M%S")
        logmessage = formatted_nowdate + " \"" + gen_dir + "\" is downloaded!\n"
        print(logmessage)
        with open(logfile_name, "a") as f:
            print(logmessage, file=f)
        # Navigate one directory up
        os.chdir("..")

    # Clean up
    driver.quit()
    print("Done!!")


if __name__ == "__main__":
    main()
