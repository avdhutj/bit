from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import keys

class BitfinexWithdrawal:
  base_url = "https://www.bitfinex.com/"
  def __init__(self):
    self.isLoggedIn = False
  def setup(self):
    self.driver = webdriver.Firefox()
    self.driver.implicitly_wait(30)
  def login(self):
    driver = self.driver
    driver.get(BitfinexWithdrawal.base_url + "/")
    driver.find_element_by_link_text("Login").click()
    driver.find_element_by_id("login").click()
    driver.find_element_by_id("login").clear()
    driver.find_element_by_id("login").send_keys(keys.BITFINEX_LOGIN)
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(keys.BITFINEX_PASS)
    driver.find_element_by_xpath("//button[@type='submit']").click()

    self.isLoggedIn = True

  def withdraw(self, withdrawal_address, amount):
    if self.isLoggedIn == False:
      print 'Called Withdrawal without loggin in'
      return False

    driver = self.driver
    driver.find_element_by_link_text("Withdraw").click()
    driver.find_element_by_css_selector("a.selector").click()
    driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div/div[3]/section/div/div/form/div[2]/div/div/ul/li[3]").click()
    driver.find_element_by_name("address").clear()
    driver.find_element_by_name("address").send_keys(withdrawal_address)
    driver.find_element_by_name("amount").clear()
    driver.find_element_by_name("amount").send_keys(str(amount))
    driver.find_element_by_xpath("//input[@value='Withdraw BTC']").click()

  def clear(self):
    self.driver.quit()
  def loginAndWithdraw(self, withdrawal_address, amount):
    self.setup()
    self.login()
    self.withdraw(withdrawal_address, amount)
    # self.clear()

if __name__ == '__main__':
  bitfinex_withdrawal(keys.BTCE_DEPOSIT_ADDRESS, 0.0)
