from selenium.webdriver.chrome.webdriver import WebDriver


from django.test import LiveServerTestCase

class TitleTest(LiveServerTestCase):

    @classmethod
    def setupClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicity_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()



    def test_title_on_homepage(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist',self.selenium.title)