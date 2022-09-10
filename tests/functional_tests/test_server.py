from selenium import webdriver
from selenium.webdriver.chrome.service import Service as CS
from selenium.webdriver.firefox.service import Service as FS
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep


class TestWebSiteFirefox:

    def setup_method(self):
        service = FS('tests/functional_tests/geckodriver')
        self.driver = webdriver.Firefox(service=service)

    def test_login(self):
        self.driver.get("http://127.0.0.1:5000")
        assert "GUDLFT" in self.driver.title
        elem = self.driver.find_element(By.NAME, "email")
        elem.send_keys("admin@irontemple.com")
        elem.send_keys(Keys.RETURN)
        sleep(5)
        assert "<h2>Welcome, admin@irontemple.com </h2>" in self.driver.page_source

    def teardown_method(self):
        self.driver.quit()


class TestWebSiteChrome:

    def setup_method(self):
        service = CS('tests/functional_tests/chromedriver')
        self.driver = webdriver.Chrome(service=service)

    def test_login(self):
        self.driver.get("http://127.0.0.1:5000")
        assert "GUDLFT" in self.driver.title
        elem = self.driver.find_element(By.NAME, "email")
        elem.send_keys("admin@irontemple.com")
        elem.send_keys(Keys.RETURN)
        sleep(5)
        assert "<h2>Welcome, admin@irontemple.com </h2>" in self.driver.page_source

    def teardown_method(self):
        self.driver.quit()

