from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Replace these with your LinkedIn credentials
LINKEDIN_USERNAME = 'mc21014@zealeducation.com'
LINKEDIN_PASSWORD = 'leomessi10'
POST_CONTENT = 'Hello, I am new on LinkedIn!'

# Initialize the Chrome driver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open LinkedIn login page
    driver.get("https://www.linkedin.com/login")

    # Log in
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    username_input.send_keys(LINKEDIN_USERNAME)
    password_input.send_keys(LINKEDIN_PASSWORD)
    login_button.click()

    # Wait for login to complete and home page to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
    )

    # Click on the "Start a post" input area
    start_post_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Start a post, try writing with AI']"))
    )
    start_post_button.click()

    # Wait for the post modal to open
    post_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
    )

    # Enter the post content
    post_input.click()
    post_input.send_keys(POST_CONTENT)

    # Click the "Post" button
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Post']"))
    )
    submit_button.click()

    print("Post created successfully!")

finally:
    # Close the browser
    driver.quit()
