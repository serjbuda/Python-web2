import unittest
from sqlalchemy.orm import Session
from app import crud, models, schemas

class TestContacts(unittest.TestCase):
    def setUp(self):
        self.db = Session()  

    def test_create_contact(self):
        contact_data = schemas.ContactCreate(name="John Doe", phone_number="+1234567890")
        contact = crud.create_contact(self.db, contact_data, user_id=1)  # replace `user_id=1` with a valid user ID
        self.assertEqual(contact.name, contact_data.name)

    def tearDown(self):
        self.db.rollback()  

if __name__ == "__main__":
    unittest.main()
