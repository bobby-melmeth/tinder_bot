from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



from login_details import email, password

class TinderBot():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        chrome_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    def open_tinder(self):
        self.driver.get('https://tinder.com')

        sleep(2)

        login = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]')
        login.click()
        sleep(1)
        self.facebook_login()

        sleep(6)
        try:
            allow_location_button = self.driver.find_element('xpath', '//*[@id="t-1917074667"]/main/div/div/div/div[3]/button[1]')
            allow_location_button.click()
        except:
            print('no location popup')

        try:
            notifications_button = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[2]')
            notifications_button.click()
        except:
            print('no notification popup')

########################################################################################################################################################################################


    def facebook_login(self):
        # Find and click FB login button
        login_with_facebook = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/main/div[1]/div/div[1]/div/div/div[2]/div[2]/span/div[2]/button/div[2]/div[2]/div/div'))
        )
        login_with_facebook.click()

        # Save reference to the main window
        base_window = self.driver.window_handles[0]

        # Wait for the Facebook popup window to appear and switch to it
        WebDriverWait(self.driver, 20).until(EC.number_of_windows_to_be(2))
        for window_handle in self.driver.window_handles:
            if window_handle != base_window:
                self.driver.switch_to.window(window_handle)
                break

        # Find and click the accept cookies button in the Facebook popup window
        cookies_accept_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input'))
        )
        cookies_accept_button.click()

        # Find and enter email, password, and click login button in the Facebook popup window
        email_field = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[1]/form/div/div[1]/div/input'))
        )
        pw_field = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[1]/form/div/div[2]/div/input'))
        )
        login_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input'))
        )

        # Enter email, password, and login
        email_field.send_keys(email)
        pw_field.send_keys(password)
        login_button.click()

        # Switch back to the main window
        self.driver.switch_to.window(base_window)


########################################################################################################################################################################################
    def right_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_RIGHT)
    def left_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_LEFT)

    def auto_swipe(self):
        while True:
            sleep(2)
            try:
                self.right_swipe()
            except:
                self.close_match()

    def close_match(self):
        match_popup = self.driver.find_element('xpath', '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()

    def get_matches(self):
        match_profiles = self.driver.find_elements('class name', 'matchListItem')
        message_links = []
        for profile in match_profiles:
            if profile.get_attribute('href') == 'https://tinder.com/app/my-likes' or profile.get_attribute('href') == 'https://tinder.com/app/likes-you':
                continue
            message_links.append(profile.get_attribute('href'))
        return message_links

    def send_messages_to_matches(self):
        links = self.get_matches()
        for link in links:
            self.send_message(link)

    def send_message(self, link):
        self.driver.get(link)
        sleep(2)
        text_area = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/textarea')

        text_area.send_keys('hi')

        text_area.send_keys(Keys.ENTER)

bot = TinderBot()
bot.open_tinder()
sleep(10)
bot.auto_swipe()
bot.send_messages_to_matches()