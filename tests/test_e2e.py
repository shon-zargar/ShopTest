import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.CheckoutPage import CheckOutPage
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass

class TestOne(BaseClass):

    def test_e2e(self):
        log = self.getLogger()
        homePage = HomePage(self.driver)
        checkoutpage = homePage.shopItems()
        log.info("Getting all the card titles")

        # Use enumerate to get both index and card
        for i, card in enumerate(checkoutpage.getCardTitles()):
            cardText = card.text
            log.info(cardText)
            if cardText == "Blackberry":
                checkoutpage.getCardFooter()[i].click()

        self.driver.find_element(By.CSS_SELECTOR, "a[class*='btn-primary']").click()

        confirmpage = checkoutpage.checkOutItems()
        log.info("Entering country name as 'ind'")
        self.driver.find_element(By.ID, "country").send_keys("ind")

        # Use explicit wait instead of time.sleep()
        country_option = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "India"))
        )
        country_option.click()

        self.driver.find_element(By.XPATH, "//div[@class='checkbox checkbox-primary']").click()
        self.driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

        # Use assert with a clear message
        success_message = self.driver.find_element(By.CSS_SELECTOR, "[class*='alert-success']").text
        log.info("Text received from application is " + success_message)
        assert "Success! Thank you!" in success_message, "Checkout was not successful"
