from selenium import webdriver
from time import sleep
from login_info import username, password
from sys import exit


class GfFinder():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.base_window = self.driver.window_handles[0]
        self.swiped = 0
        self.matches = 0

    def login(self):
        try:
            self.driver.get('https://www.tinder.com')

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
            sleep(2)
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
            sleep(2)
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
        except Exception:
            print('Error logging in')
            self.gf_limit()

    def swipe(self):
        like = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]'
        )
        like.click()

    def auto_swipe(self):
        while True:
            sleep(0.5)

            try:
                self.swipe()
                self.swiped += 1
            except Exception:
                try:
                    # out of likes
                    _ = self.driver.find_element_by_xpath(
                        '//*[@id="modal-manager"]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/div/span/div/h3'
                    )
                    self.swiped -= 1
                    break
                except Exception:
                    try:
                        # asking if I want to add Tinder to homescreen
                        no_homescreen = self.driver.find_element_by_xpath(
                            '//*[@id="modal-manager"]/div/div/div[2]/button[2]'
                        )
                        no_homescreen.click()
                        continue
                    except Exception:
                        try:
                            # its a match! :)
                            close_match = self.driver.find_element_by_xpath(
                                '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a'
                            )
                            self.matches += 1
                            close_match.click()
                            continue
                        except Exception as e:
                            # something went wrong
                            print(f'Something went wrong: {e}')
                            break

        self.gf_limit()

    def gf_limit(self):
        self.driver.close()
        print(f'Total Swipes: {gfs.swiped}\nTotal Matches: {gfs.matches}')
        exit()


if __name__ == '__main__':
    gfs = GfFinder()
    gfs.login()
    sleep(5)
    gfs.auto_swipe()
