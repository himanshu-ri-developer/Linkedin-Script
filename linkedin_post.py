import time
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class LinkedinLogin:
    def __init__(self, browser):
        env_file = os.path.join(Path(__file__).parent.parent, ".env")
        load_dotenv(env_file)
        self.browser = browser
        self.username = os.getenv("LINKEDIN_USERNAME")
        self.password = os.getenv("LINKEDIN_PASSWORD")
        logging.info(f'Username: {self.username}')

    def login_and_open_notifications(self):
        try:
            self.browser.get("https://www.linkedin.com/login")
            self._perform_login()

            time.sleep(2)  # Wait for the page to load

            # Navigate to notifications
            notifications_tab = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Notifications']"))
            )
            self.browser.execute_script("arguments[0].click();", notifications_tab)
            time.sleep(5)  # Adjust sleep time as needed to wait for notifications to load

            logging.info("Successfully navigated to Notifications tab!")

        except Exception as e:
            logging.error(f"Error during login and navigation: {e}")
            raise e

    def _perform_login(self):
        try:
            self.browser.implicitly_wait(10)
            time.sleep(2)
            username_field = self.browser.find_element(By.ID, "username")
            username_field.send_keys(self.username)
            time.sleep(2)

            password_field = self.browser.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            time.sleep(3)
            password_field.send_keys(Keys.RETURN)

            # Wait for 2FA input (manually enter OTP if needed)
            logging.info("Please complete the login process, including any 2FA if required...")
            WebDriverWait(self.browser, 60).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
            )
            logging.info("Login completed successfully.")
        except Exception as e:
            logging.error(f"Error during login: {e}")
            raise e

if __name__ == "__main__":
    # Initialize the Chrome driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        linkedin_login = LinkedinLogin(driver)
        linkedin_login.login_and_open_notifications()

        # Wait for 1 minute on the LinkedIn notifications page
        logging.info("Waiting for 1 minute on the LinkedIn notifications page...")
        time.sleep(60)
        logging.info("Finished waiting. Exiting...")
    finally:
        # Close the browser
        driver.quit()
