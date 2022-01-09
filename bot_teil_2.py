from selenium import webdriver
from data import username, password
import time
import os
import requests
from selenium.webdriver.common.proxy import Proxy, ProxyType


class Instagrambot():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('chromedriver/chromedriver')

    def close_browser(self):
        self.driver.close()
        self.driver.quit()

    def login(self):
        driver = self.driver
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

        driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button').click()
        time.sleep(10)

    def like_photos_by_hastag(self, hashtag):
        driver = self.driver

        driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(3)

        for i in range(1, 4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(4)

        links = driver.find_elements_by_tag_name('a')
        post_url = [item.get_attribute('href') for item in links if "/p/" in item.get_attribute('href')]

        #
        # for link in links:
        #     href = link.get_attribute('href')
        #
        #     if "/p/" in href:
        #         post_url.append(href)

        print(post_url)

        for url in post_url:
            try:
                driver.get(url)
                time.sleep(3)
                driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
                time.sleep(60)
            except Exception as ex:
                print(ex)
                self.close_browser()

    def get_all_posts_url(self, userpage):
        driver = self.driver
        driver.get(userpage)
        time.sleep(4)

        posts_count = int(
            driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text)
        loops_count = int(posts_count / 12)

        posts_urls = []

        for i in range(0, loops_count):
            hrefs = driver.find_elements_by_tag_name('a')
            hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

            for href in hrefs:
                posts_urls.append(href)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(4)

        set_posts_urls = set(posts_urls)
        file_name = userpage.split("/")[-2]
        if not os.path.isfile(f'{file_name}.txt'):
            with open(f'{file_name}.txt', 'a') as file:
                for posts_url in set_posts_urls:
                    file.write(posts_url + "\n")

    def put_likes(self, userpage):
        driver = self.driver
        self.get_all_posts_url(userpage)
        file_name = userpage.split("/")[-2]
        driver.get(userpage)
        time.sleep(4)

        with open(f'{file_name}.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list:
                try:
                    driver.get(post_url)
                    time.sleep(3)
                    like_button = driver.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button')
                    like_svg_label = like_button.find_element_by_tag_name('svg').get_attribute('aria-label')

                    print(like_svg_label)
                    if 'Gefällt mir' == like_svg_label:
                        like_button.click()

                    time.sleep(60)
                except Exception as ex:
                    print(ex)

                    self.close_browser()

    def xpath_exist(self, xpath):
        driver = self.driver
        try:
            driver.find_element_by_xpath(xpath)
            exist = True
        except Exception:
            exist = False

        return exist

    def download_posts(self, userpage):
        driver = self.driver
        driver.get(userpage)
        file_name = userpage.split("/")[-2]

        if os.path.exists(file_name):
            print('Ordner existiert')
        else:
            os.mkdir(file_name)

        multiple_img_path = '/html/body/div[1]/section/main/div/div[1]/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/img'
        single_img_path = '/html/body/div[1]/section/main/div/div[1]/article/div/div[1]/div/div/div[1]/img'

        if os.path.isfile(f'{file_name}.txt'):
            with open(f'{file_name}.txt') as file:

                url_list = file.readlines()

                for post_url in url_list:
                    try:
                        driver.get(post_url)
                        time.sleep(4)
                        post_id = post_url.split('/')[-2]

                        if self.xpath_exist(multiple_img_path):
                            img_src = driver.find_element_by_xpath(multiple_img_path).get_attribute('src')
                            print('Download Multiple')
                        elif self.xpath_exist(single_img_path):
                            img_src = driver.find_element_by_xpath(single_img_path).get_attribute('src')
                            print('Download Single')
                        else:
                            try:
                                img_src = driver.find_element_by_xpath(
                                    '/html/body/div[1]/section/main/div/div[1]/article/div/div[1]').find_element_by_tag_name(
                                    'img').get_attribute('src')
                            except Exception:
                                continue

                        img_data = requests.get(img_src)

                        with open(f"{file_name}/{post_id}_img.jpg", "wb") as img_file:
                            if img_data:
                                img_file.write(img_data.content)
                            else:
                                print('Download nicht möglich')

                    except Exception as ex:
                        print(ex)
                        print('dowload')
        else:
            self.get_all_posts_url(userpage)

    def follow_users(self, userpage):

        driver = self.driver
        driver.get(userpage)
        time.sleep(4)

        file_name = userpage.split("/")[-2]

        if os.path.exists(file_name):
            print('Ordner existiert')
        else:
            os.mkdir(file_name)

        followers_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
        followers_count = int( driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title').replace('.', ''))

        iterations = int (followers_count/12)

        followers_button.click()
        time.sleep(2)

        followers_list = driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/ul')
        followers_list_container = driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]')

        print(f"iterations {iterations}")
        try:
            follower_links = []
            for i in range(0, iterations + 1):
                driver.execute_script("arguments[1].scrollTop = arguments[1].scrollHeight", followers_list, followers_list_container)
                time.sleep(2)
                print(f'Iteration {i}')

            all_links = followers_list.find_elements_by_tag_name("li")

            for link in all_links:
                link = link.find_element_by_tag_name('a').get_attribute('href')
                follower_links.append(link)

            with open(f"{file_name}/{file_name}_followers.txt", "a") as file:
                for link in follower_links:
                    file.write(link + "\n")

            # with open(f"{file_name}/{file_name}_followers.txt") as file:
            #     user_urls = file.readlines()
            #
            #     for url in user_urls:
            #         try:
            #             driver.get(url)
            #         except Exception:
            #             print('Ex')
            #             driver.close()


        except Exception as ex:
            print(ex)

bot = Instagrambot(username, password)
bot.login()
bot.follow_users('https://www.instagram.com/dimiweb_codeacademy/')
# bot.download_posts('https://www.instagram.com/leana.dima/')
# bot.put_likes("https://www.instagram.com/leana.dima/")
# bot.close_browser()
