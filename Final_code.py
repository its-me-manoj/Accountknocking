
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from colorama import Fore, init
from selenium.common.exceptions import TimeoutException
import sys
from validate_email_address import validate_email

if not sys.stdout.isatty():
    init(strip=True)


def is_valid_email(email):
    return validate_email(email)


def check_website(emails, website_url, website_name, email_input_locator, submit_button_locator, error_message_locator,
                  success_message_locator, available_accounts, unavailable_accounts):
    chrome_options = Options()

    driver_path = ChromeDriverManager().install()

    service = Service(executable_path=driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        website_available_accounts = []
        website_unavailable_accounts = []

        for email in emails:
            if not is_valid_email(email):
                print(f"Invalid email: {email}")
                continue

            driver.get(website_url)

            email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(email_input_locator))
            email_input.send_keys(email)

            if submit_button_locator is not None:
                submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button_locator))
                submit_button.click()
            else:
                email_input.submit()

            time.sleep(4)

            if website_name.lower() == 'spotify' or website_name.lower() == 'bbc':
                try:
                    error_message_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(error_message_locator))

                    error_message = error_message_element.text

                    website_available_accounts.append(email)

                except TimeoutException:
                    website_unavailable_accounts.append(email)
                    website_available_accounts.append("doesn't exit")

            else:
                try:
                    error_message_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(error_message_locator))

                    error_message = error_message_element.text
                    website_unavailable_accounts.append(email)
                    website_available_accounts.append("doesn't exit")
                except TimeoutException:
                    website_available_accounts.append(email)

   
        available_accounts[website_name] = website_available_accounts
        unavailable_accounts[website_name] = website_unavailable_accounts

    finally:
        driver.quit()


websites = [
    {
        'name': 'Spotify',
        'url': 'https://www.spotify.com/in-en/signup/',
        'email_locator': (By.ID, 'username'),
        'submit_locator': None,  # Spotify uses Enter key for submission
        'error_locator': (By.XPATH,"//span[contains(@class, 'Message-sc-15vkh7g-0') and contains(@class, 'kxWrWw')]"),
        'success_message': None,
    },
    {
        'name': 'Pinterest',
        'url': 'https://in.pinterest.com/login/',
        'email_locator': (By.ID, 'email'),
        'submit_locator': None,  # Pinterest uses Enter key for submission
        'error_locator': (By.XPATH, "//div[contains(text(), 'The email you entered does not belong to any account.')]"),
     }
     ,
     {
        'name': 'BBC',
        'url': 'https://account.bbc.com/auth?realm=%2F&clientId=Account&context=homepage&ptrt=https%3A%2F%2Fwww.bbc.com%2F&userOrigin=HOMEPAGE_GNL&isCasso=false&action=sign-in&redirectUri=https%3A%2F%2Fsession.bbc.com%2Fsession%2Fcallback%3Frealm%3D%2F&service=IdSignInService&nonce=5UCDlkyl-UQGkyOvEgRvx6Hd8xy7LqZOVIv0',
        'email_locator': (By.ID, 'user-identifier-input'),
        'submit_locator': (By.ID, 'submit-button'),
        'error_locator': (By.XPATH, "//div[@id='form-message-general']/p[@class='sb-form-message__text']/span/span/a[@class='link']"),
     },
     {
        'name': 'Scroll',
        'url': 'https://scroll.in/signin',
        'email_locator': (By.ID, 'emailAddress'),
        'submit_locator': (By.XPATH, "//button[@class='button']/span[text()='Sign in']"),
        'error_locator': (By.XPATH, "//p[contains(text(), 'We couldn’t find any active Scroll Membership linked to the email address you entered. Please check the email and try again.')]"),
     },
    {
        'name': 'Amazon',
        'url': 'https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Feu.primevideo.com%2Fregion%2Feu%2Fauth%2Freturn%2Fref%3Dav_auth_ap%3F_t%3Dsg45dnPiqyhyTdJwB4cvkU03GHc08Y_wbpvIis2YfBc20AAAAAQAAAABlkTw7cmF3AAAAAPgWC9WfHH8iB-olH_E9xQ%26location%3D%2Fregion%2Feu%2F%3Fref_%253Datv_auth_pre&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&accountStatusPolicy=P1&openid.assoc_handle=amzn_prime_video_sso_in&openid.mode=checkid_setup&siteState=258-8435775-3084124&language=en_US&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0',
        'email_locator': (By.ID, 'ap_email'),
        'submit_locator': (By.ID, 'continue'),
        'error_locator': (By.XPATH, "//*[@id='auth-error-message-box']"),
    }

]

emails_to_check = [
    'kabilramesh@gmail.com',
    'manojkumar.mr.cce@gmail.com'
]

available_accounts = {}
unavailable_accounts = {}



for website in websites:
    check_website(emails_to_check, website['url'], website['name'], website['email_locator'], website['submit_locator'],
                  website['error_locator'], website.get('success_message'), available_accounts, unavailable_accounts)

for website, accounts in available_accounts.items():
    print(f"\nAvailable Accounts for {website}:")
    for account in accounts:
        print(account)
        sys.stdout.flush()
        time.sleep(0.1)

for website, accounts in unavailable_accounts.items():
    print(f"\nUnavailable Accounts for {website}:")
    for account in accounts:
        print(account)
        sys.stdout.flush()
        time.sleep(0.1)

##streamlit
print(available_accounts)
df = pd.DataFrame(available_accounts)
st.write(df)

