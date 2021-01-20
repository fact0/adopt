from unittest import TestCase

from app import app
from models import db, Pet

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users class."""

    def setUp(self):
        """Clean up any existing users."""

        Pet.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_create_pet(self):
        p1 = Pet(name="Pet One", species="dog", age="5", available=True)
        db.session.add(p1)
        db.session.commit()

        self.assertEqual(p1.name, "Pet One")
        self.assertEqual(p1.species, "dog")

    def test_edit_user(self):
        p1 = Pet(name="Pet One", species="dog", age="5", available=True)
        db.session.add(p1)
        db.session.commit()

        p1.name = "Pet Two"
        p1.species = "cat"
        db.session.commit()

        self.assertEqual(p1.name, "Pet Two")
        self.assertEqual(p1.species, "cat")
