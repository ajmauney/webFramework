import unittest, sys

sys.path.append('../webFramework') # imports python file from parent directory
from new import app #imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_home_page(self):
      response = self.app.get('/home',follow_redirects=True)
      self.assertEqual(response.status_code,200)
      
    def test_new_page(self):
      response = self.app.get('/new',follow_redirects=True)
      self.assertEqual(response.status_code,200)

if __name__ == "__main__":
    unittest.main()
