import unittest
from sqlalchemy.orm import Session
from app import crud, models, schemas

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.db = Session()  

    def test_create_user(self):
        user_data = schemas.UserCreate(email="test@example.com", password="password")
        user = crud.create_user(self.db, user_data)
        self.assertEqual(user.email, user_data.email)

    def tearDown(self):
        self.db.rollback()

if __name__ == "__main__":
    unittest.main()
