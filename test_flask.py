from unittest import TestCase

from app import app
from models import db, Pet

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class PetTestCase(TestCase):
    """Tests for user routes."""

    def setUp(self):
        """Add sample users."""

        Pet.query.delete()

        p1 = Pet(name="Pet One", species="dog", age="5", available=True)
        p2 = Pet(name="Pet Two", species="cat", age="1", available=True)
        p3 = Pet(name="Pet Three", species="porcupine",
                 age="30", available=False)
        db.session.add_all([p1, p2, p3])
        db.session.commit()

        self.pet_id = p1.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Pet Adoption Site', html)
            self.assertIn('Pet One', html)
            self.assertIn('Pet Two', html)
            self.assertIn('Pet Three', html)

    def test_404_page(self):
        with app.test_client() as client:
            resp = client.get("/notapet")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 404)
            self.assertIn('404 Pet not found', html)

    def test_pet_details(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.pet_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Pet One', html)

    def test_render_add_pet_form(self):
        with app.test_client() as client:
            resp = client.get("/add")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add a Pet', html)

    def test_add_pet_form(self):
        with app.test_client() as client:
            d = {"name": "Pet Four", "species": "cat", "age": "4", "available": "True"}
            resp = client.post("/add", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Pet Four", html)

    def test_render_edit_pet_form(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.pet_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit a Pet', html)

    def test_edit_pet_form(self):
        with app.test_client() as client:
            d = {"name": "Pet Four", "species": "cat", "age": "4", "available": "True"}
            resp = client.post(f"/{self.pet_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Pet Four", html)

