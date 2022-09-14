from selenium import webdriver
from selenium.webdriver.chrome.service import Service as CS
from selenium.webdriver.firefox.service import Service as FS
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestWebSiteFirefox:

    def setup_method(self):
        service = FS('tests/functional_tests/geckodriver')
        self.driver = webdriver.Firefox(service=service)
        self.driver.get("http://127.0.0.1:5000")
        WebDriverWait(self.driver, timeout=5).until(EC.title_is("GUDLFT Registration"))
        assert "Registration" in self.driver.title

    def test_user_story_happy_end(self):
        """
        Parcours client #HappyEnd (site Flask on-line)
            - Identification
            - Choix de la compétition
            - Réservation des places
            - Affichage Dashboard
            - Déconnexion
        """
        club_email = "admin@irontemple.com"
        places_required = "1"

        main_windows = self.driver.current_window_handle
        self.driver.find_element(By.NAME, "email").send_keys(club_email + Keys.RETURN)
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains("Summary"))
        assert "Welcome, " + club_email in self.driver.page_source

        self.driver.find_elements(By.LINK_TEXT, "Book Places")[0].click()
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains("Booking"))
        assert "Booking for" in self.driver.title

        self.driver.find_element(By.NAME, "places").send_keys(places_required + Keys.RETURN)
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains("Summary"))
        assert "Great-booking complete!" in self.driver.page_source

        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        self.driver.switch_to.window("dashboard")
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains("Dashboard"))
        assert "Dashboard" in self.driver.title

        self.driver.switch_to.window(main_windows)
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        WebDriverWait(self.driver, timeout=5).until(EC.title_is("GUDLFT Registration"))
        assert "Registration" in self.driver.title

    def teardown_method(self):
        self.driver.quit()


class TestWebSiteChrome:

    def setup_method(self):
        service = CS('tests/functional_tests/chromedriver')
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("http://127.0.0.1:5000")
        WebDriverWait(self.driver, timeout=5).until(EC.title_is("GUDLFT Registration"))
        assert "Registration" in self.driver.title

    def test_user_story_bad_trip(self):
        """
        Parcours client #BadTrip (site Flask on-line)
            - Identification (échec : adresse mail inexistante)
            - Identification
            - Choix de la compétition (échec : date de la compétition dépassée)
            - Choix de la compétition
            - Réservation des places (échec : nombre négatif de places)
            - Réservation des places (échec : pas assez de points)
            - Affichage Dashboard
            - Déconnexion
        """
        club_email = "john@simplylift.co"

        main_windows = self.driver.current_window_handle
        self.driver.find_element(By.NAME, "email").send_keys("wrong@email" + Keys.RETURN)
        WebDriverWait(self.driver, timeout=5).until(EC.title_is("GUDLFT Registration"))
        assert "Wrong email, please try again" in self.driver.page_source

        self.driver.find_element(By.NAME, "email").send_keys(club_email + Keys.RETURN)
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains("Summary"))
        assert "Welcome, " + club_email in self.driver.page_source

        self.driver.find_elements(By.LINK_TEXT, "Book Places")[1].click()
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains("Summary"))
        assert "You cannot book a past competition" in self.driver.page_source

        self.driver.find_elements(By.LINK_TEXT, "Book Places")[0].click()
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains("Booking"))
        assert "Booking for" in self.driver.title

        places_required = "-2"
        self.driver.find_element(By.NAME, "places").send_keys(places_required + Keys.RETURN)
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains("Booking"))
        assert "You need to book a positive integer of places" in self.driver.page_source

        places_required = "20"
        self.driver.find_element(By.NAME, "places").send_keys(places_required + Keys.RETURN)
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains("Summary"))
        assert "Not enough points to book so many places" in self.driver.page_source

        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        self.driver.switch_to.window("dashboard")
        WebDriverWait(self.driver, timeout=5).until(EC.title_contains("Dashboard"))
        assert "Dashboard" in self.driver.title

        self.driver.switch_to.window(main_windows)
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        WebDriverWait(self.driver, timeout=5).until(EC.title_is("GUDLFT Registration"))
        assert "Registration" in self.driver.title

    def teardown_method(self):
        self.driver.quit()
