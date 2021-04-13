#!/usr/bin/python3
"""
ZohoCRM - Backup Scraper.

Written by: Dylan Griffiths & Smit Patel
Created: 2021-04-09

API:
- signIn
    ** Required to be called before scraping can occur.

- fetchAuditLog
    ** Gets the audit log from CRM.
    => https://crm.zoho.com/crm/org685568171/settings/auditlog
    => Must find and select the "Export Audit Log" link
            <a href="javascript:;" onclick="auditLog.exportAuditLog();" class="f14" data-zcqa="dash_exportAuditLog"><u>Export Audit Log</u></a>
    => Must wait for the export to complete, then find and click the download button when the export is complete.
        <a class="fR bt-smallnewgraybtn newgraybtn downloadlink_report" style="cursor: pointer;" href="/crm/org685568171/Export.do?action=Download&amp;module=AuditLog&amp;uniqueID=3869165000024775001">Download</a>


- fetchCRMFunctions
    ** Exports functions from CRM.



"""


from selenium import webdriver
from config import *
import time
from pyotp import *
# from parsel import Selector
# from bs4 import BeautifulSoup
# import json
# from selenium.webdriver.common.keys import Keys

##

class ZohoCRMBackupScraper:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')  # required when running as root user. otherwise you would get no sandbox errors.
        # chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('./chromedriver-89/chromedriver', options=chrome_options)
                                       #service_args=['--verbose', '--log-path=chromedriver-zohocrm.log'])

    def ifExist(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
            return True
        except:
            return False

    # opens linked in webpage, and signs in
    # the login info must be stored in the config file
    def signIn(self):
        self.driver.get("https://accounts.zoho.com/signin")

        # <input
        # id = "login_id"
        # placeholder = "Email address or mobile number"
        # value = ""
        # type = "email"
        # name = "LOGIN_ID"
        # class ="textbox" required="" onkeypress="clearCommonError('login_id')" onkeyup="checking()" onkeydown="checking()" autocapitalize="off" autocomplete="on" autocorrect="off" tabindex="1" >

        if self.ifExist("//form[1]"):
            self.driver.find_element_by_id('login_id').send_keys(loginInfo["email"])
            time.sleep(1)
            self.driver.find_element_by_id('nextbtn').click()
            time.sleep(1)
            self.driver.find_element_by_id('password').send_keys(loginInfo["password"])
            time.sleep(1)
            self.driver.find_element_by_id('nextbtn').click()
            time.sleep(6)
            # try:
            #     # locate OTP field
            #     otp_placeholder = self.driver.find_element_by_id(
            #         "input__phone_verification_pin")  # ("/html/body/main/section[1]/div[2]/form")
            #     print("found 2fa verification")
            #     # creating tokens to send OTP
            #     token = totp.now()
            #     otp_placeholder.send_keys(token)
            #     submit_button = self.driver.find_element_by_id(
            #         "two-step-submit-button")  # ("/html/body/main/section[1]/div[2]/form/button")
            #     submit_button.click()
            # except:
            #     print(" 2FA authentication not required or failed to complete 2FA ")
            time.sleep(42)
            print("Successfully logged in!")
        else:
            print("Error logging in!")


        # # locate login button and click it
        # login_button = self.driver.find_element_by_xpath("/html/body/main/section[1]/div[2]/form/button")
        # login_button.click()
        # try :
        #     # locate OTP field
        #     otp_placeholder = self.driver.find_element_by_id("input__phone_verification_pin") #("/html/body/main/section[1]/div[2]/form")
        #     print("found 2fa verification")
        #     #creating tokens to send OTP
        #     token = totp.now()
        #     otp_placeholder.send_keys(token)
        #     submit_button = self.driver.find_element_by_id("two-step-submit-button") #("/html/body/main/section[1]/div[2]/form/button")
        #     submit_button.click()
        # except :
        #     print(" 2FA authentication not required or failed to complete 2FA ")



def main():
    scraper = ZohoCRMBackupScraper()
    scraper.signIn()
    scraper.fetchAuditLog()

if __name__ == "__main__":
    main()