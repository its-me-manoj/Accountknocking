from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from colorama import Fore
from selenium.common.exceptions import TimeoutException

def sign_up(emails):
    # Create an instance of Options
    chrome_options = Options()

    # Get the path to the driver executable
    driver_path = ChromeDriverManager().install()

    # Create a Service instance with the driver path
    service = Service(executable_path=driver_path)

    # Initialize the WebDriver with the Service instance and options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        for email in emails:
            driver.get("https://scroll.in/signin")

            # Wait until the email input field is present and send keys to it
            email_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "emailAddress")))
            email_input.send_keys(email)

            # Click the "Sign In" button
            sign_in_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button']/span[text()='Sign in']")))
            sign_in_button.click()

            time.sleep(4)

            try:
                # Update the XPath for the error message
                error_message_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'We couldn’t find any active Scroll Membership linked to the email address you entered. Please check the email and try again.')]")))
                error_message = error_message_element.text
                print(Fore.YELLOW + f'This "{email}" doesn\'t exist in scroll. {error_message}')
            except TimeoutException:
                print(Fore.GREEN + f'This address is already linked to an existing account for {email}.')

    finally:
        driver.quit()


emails_to_check =['nagasharmilaperumal@gmail.com','nagasharmila.p2021cce@sece.ac.in']
sign_up(emails_to_check)
