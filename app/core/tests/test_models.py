from decimal import Decimal
from unittest.mock import patch
from core import models
from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email="user@example.com", password="testpass123"):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@example.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ("test1@EXAMPLE.COM", "test1@example.com"),
            ("Test2@Example.com", "Test2@example.com"),
            ("TEST3@example.com", "TEST3@example.com"),
            ("test4@example.com", "test4@example.com"),
        ]
        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email, "test123")
            self.assertEqual(user.email, expected_email)

    def test_new_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            "test@example.com",
            "testpass123",
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title="Steak and mushroom sauce",
            time_minutes=5,
            price=Decimal("5.00"),
            description="This is a test description",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(
            user=user,
            name="Vegan",
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredeint(self):
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name="Cucumber",
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch("core.models.uuid.uuid4")
    def test_recipe_file_name_uuid(self, mock):
        uuid = "test-uuid"
        mock.return_value = uuid
        file_path = models.recipe_image_file_path(None, "myimage.jpg")

        expected_path = f"uploads/recipe/{uuid}.jpg"
        self.assertEqual(file_path, expected_path)
