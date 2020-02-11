from selenium import webdriver
from time import sleep
from login_info import username, password
from sys import exit
from os import system


class Controller():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.base_window = self.driver.window_handles[0]
        self.swiped = 0
        self.r_swipes = 0
        self.l_swipes = 0
        self.matches = 0

    def login(self):
        try:
            self.driver.get('https://www.tinder.com')
            sleep(1)
            login_btn = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/header/div[1]/div[2]/div/button/span'
            )
            login_btn.click()
            sleep(0.5)

            login_fb = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div/div/div/div[3]/div[2]/button/span'
            )
            login_fb.click()

            # login in Facebook popup
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])

            login_email = self.driver.find_element_by_xpath(
                '//*[@id="email"]'
            )
            login_email.send_keys(username)

            login_pass = self.driver.find_element_by_xpath(
                '//*[@id="pass"]'
            )
            login_pass.send_keys(password)

            submit = self.driver.find_element_by_xpath(
                '//*[@id="u_0_0"]'
            )
            submit.click()

            # back to base window
            sleep(1)
            self.driver.switch_to.window(self.base_window)

            allow_loc = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div/div/div/div[3]/button[1]'
            )
            allow_loc.click()
            sleep(0.5)

            no_noti = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div/div/div/div[3]/button[2]/span'
            )
            no_noti.click()

            try:
                no_email_confm = self.driver.find_element_by_xpath(
                    '//*[@id="modal-manager"]/div/div/div[2]/div[2]/button[2]'
                )
                no_email_confm.click()
            except Exception:
                pass

        except Exception:
            print('Error logging in.')
            self.gf_limit()

    def swipe(self):
        like = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]'
        )
        like.click()
        self.r_swipes += 1

    def swipe_left(self):
        dislike = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]'
        )
        dislike.click()
        self.l_swipes += 1

    def swipe_left_mobile(self):
        dislike = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/div/main/div/div[1]/div/div[2]/button[1]'
        )
        dislike.click()
        self.l_swipes += 1

    def auto_swipe(self):
        x = 0
        while x <= 10:
            sleep(0.5)

            try:
                self.swipe()
                self.swiped += 1
                x += 1
            except Exception:
                try:
                    self.out_of_likes()  # out of likes
                    self.swiped -= 1
                    break
                except Exception:
                    try:
                        # asking if I want to add Tinder to homescreen
                        self.home_screen()
                        continue
                    except Exception:
                        try:
                            # asking if I want Tinder Gold
                            self.tinder_gold()
                            continue
                        except Exception:
                            try:
                                # its a match! :)
                                self.match()
                                self.matches += 1
                                continue
                            except Exception as e:
                                print(f'Something went wrong: {e}')
                                break

        self.gf_limit()

    def out_of_likes(self):
        _ = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div/span/div/h3'
        )

    def out_of_likes_mobile(self):
        _ = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div[3]/button[2]'
        )

    def home_screen(self):
        no_homescreen = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div[2]/button[2]'
        )
        no_homescreen.click()

    def home_screen_mobile(self):
        no_homescreen = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div[2]/button[2]'
        )
        no_homescreen.click()

    def tinder_gold(self):
        no_gold = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div[3]/button[2]'
        )
        no_gold.click()

    def match(self):
        close_match = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a'
        )
        close_match.click()

    def gf_limit(self):
        self.driver.close()
        print(f'Total Swipes: {self.swiped}\nTotal Matches: {self.matches}')
        exit()
