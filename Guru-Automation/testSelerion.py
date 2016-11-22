import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class pythonClassSearch(unittest.TestCase) :

    def setUp(self):
        self.driver = webdriver.Chrome("/Users/laveeshrohra/Downloads/chromedriver")

    def test_python_search(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python",driver.title)
        elem = driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__" :
    unittest.main()