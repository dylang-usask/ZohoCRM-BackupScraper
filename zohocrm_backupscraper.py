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


class ZohoCRMBackupScraper:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # You'll want to change this folder to the location where you want to have the file 'Audit Log.csv' saved to.
        prefs = {'download.default_directory': '/Users/dylang/Documents/ButterMilk-Projects/AetherAutomation/kaizen-2021/ZohoCRM-BackupScraper'}
        chrome_options.add_experimental_option('prefs', prefs)

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
        if self.ifExist("//form[1]"):
            self.driver.find_element_by_id('login_id').send_keys(loginInfo["email"])
            time.sleep(1)
            self.driver.find_element_by_id('nextbtn').click()
            time.sleep(1)
            self.driver.find_element_by_id('password').send_keys(loginInfo["password"])
            time.sleep(1)
            self.driver.find_element_by_id('nextbtn').click()
            print("Successfully logged in!")
        else:
            print("Error logging in!")


    def fetchAuditLog(self):
        # It seems that it can take a couple of calls to load the page before it actually loads.
        self.driver.get("https://crm.zoho.com/crm/org685568171/settings/auditlog")
        self.driver.get("https://crm.zoho.com/crm/org685568171/settings/auditlog")


        # -- This did not work to trigger the export of the audit log:
        # self.driver.execute_script("auditLog.exportAuditLog();")

        # This does work for triggering the export of the audit log:
        print("AuditLog Page Loading")
        time.sleep(6)
        audit_log_link = self.driver.find_element_by_link_text("Export Audit Log")
        # audit_log_link = self.driver.find_element_by_partial_link_text("Export Audit Log")
        print("audit_log_link = ")
        print(audit_log_link)
        audit_log_link.click()
        time.sleep(20)
        # self.driver.save_screenshot('screenshot.png')
        download_audit_log_link = self.driver.find_element_by_link_text("Download")
        print("download_audit_log_link = ")
        print(download_audit_log_link)
        download_audit_log_link.click()
        time.sleep(42)


def main():
    scraper = ZohoCRMBackupScraper()
    scraper.signIn()
    scraper.fetchAuditLog()

if __name__ == "__main__":
    main()