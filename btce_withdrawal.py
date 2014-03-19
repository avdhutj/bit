from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import keys

class BTCEWithdrawal:
	base_url = 'http://www.btc-e.com'

	def __init__(self):
		self.isLoggedIn = False
	def setup(self):
		# Create a new instance of the Firefox driver
		driver = webdriver.Firefox()
		# go to the btc-e home page
		driver.get("http://www.btc-e.com")
		self.driver = driver

	def login(self):

		print 'Loggin In'
		driver = self.driver
		# find the element that's name attribute is 'email', i.e the log in query space
		inputElement = driver.find_element_by_name("email")
		# type in the username
		inputElement.send_keys(keys.BTCE_LOGIN)
		# find the element that's name attribute is q (the google search box)
		inputElement = driver.find_element_by_name("password")
		# type in the password
		inputElement.send_keys(keys.BTCE_PASS)
		# submit the login credentials
		inputElement.submit()
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mes_count")))
		self.isLoggedIn = True

	def withdraw(self, withdrawal_address, amount):

		print 'Withdrawing'
		driver = self.driver
		driver.get("https://btc-e.com/profile#funds/withdraw_coin/1")
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "address")))
		inputElement = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[14]/div/table/tbody/tr[3]/td[2]/input")
		inputElement.send_keys(withdrawal_address)
		#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "address")))
		inputElement = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[14]/div/table/tbody/tr[4]/td[2]/input")
		inputElement.send_keys(str(amount))
		driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[14]/div/a").click()
		driver.implicitly_wait(20)

	def go(self, link):
		self.driver.get(link)

	def clear(self):
		self.driver.clear()

	def loginAndWithdraw(self, withdrawal_address, amount):
		self.setup()
		self.login()
		self.withdraw(withdrawal_address, amount)
		# self.clear()
