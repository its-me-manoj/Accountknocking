from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyautogui
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
            driver.get("https://in.pinterest.com/login/")

            # Wait until the email input field is present and send keys to it
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
            time.sleep(4)

            pyautogui.press('enter')
            try:
                error_message_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'The email you entered does not belong to any account.')]")))
                error_message = error_message_element.text
                print(f'Error message for {email}: {error_message}')
                print(Fore.YELLOW + f'This "{email}" doesn\'t exist in Pinterest')
            except TimeoutException:
                print(Fore.GREEN + f'This address is already linked to an existing account for {email}.')

    finally:
        driver.quit()

emails_to_check = ['nagasharmila.p2021cce@sece.ac.in', 'test@example.com', 'raja@saptanglabs.com']
sign_up(emails_to_check)
