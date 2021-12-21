from selenium import webdriver
from data import username, password
import time

# def login(username, password):
#     driver=webdriver.Chrome('chromedriver/chromedriver')
#     driver.get('https://instagram.com')
#     time.sleep(3)
#     driver.find_element_by_xpath('/html/body/div[4]/div/div/button[1]').click()
#     time.sleep(2)
#     username_input = driver.find_element_by_name('username')
#     password_input = driver.find_element_by_name('password')
#     username_input.clear()
#     username_input.send_keys(username)
#     time.sleep(1)
#     password_input.clear()
#     password_input.send_keys(password)
#     time.sleep(2)
#
#     driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button').click()
#     time.sleep(10)
#
#     driver.close()
#     driver.quit()

#login(username, password)

def hashtag_search(username, password, hastag):
    driver=webdriver.Chrome('chromedriver/chromedriver')
    driver.get('https://instagram.com')
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[4]/div/div/button[1]').click()
    time.sleep(2)
    username_input = driver.find_element_by_name('username')
    password_input = driver.find_element_by_name('password')
    username_input.clear()
    username_input.send_keys(username)
    time.sleep(1)
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(2)

    driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button').click()
    time.sleep(10)

    driver.get(f'https://www.instagram.com/explore/tags/{hastag}/')
    time.sleep(3)

    # for i in range(1, 4):
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #     time.sleep(4)

    links = driver.find_elements_by_tag_name('a')
    post_url = []

    for link in links:
        href = link.get_attribute('href')

        if "/p/" in href:
            post_url.append(href)

    print(post_url)

    for url in post_url:
        driver.get(url)
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
        time.sleep(60)

    driver.close()
    driver.quit()

hashtag_search(username, password, 'food')