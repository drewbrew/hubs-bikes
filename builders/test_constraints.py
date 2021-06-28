from django.test import TestCase
from django.db.utils import IntegrityError

from .models import Guardian


class GuardianConstraintTest(TestCase):
    def test_email_not_phone(self):
        Guardian.objects.create(email="user@example.com", name="somebody")

    def test_phone_not_email(self):
        Guardian.objects.create(
            phone_number="256-555-1212",
            name="somebody",
        )

    def test_neither_email_nor_phone(self):
        with self.assertRaises(IntegrityError):
            Guardian.objects.create(
                name="somebody",
            )

    def test_email_and_phone(self):
        Guardian.objects.create(
            phone_number="256-555-1212",
            email="user@example.com",
            name="somebody",
        )

    def test_partial_address(self):
        with self.assertRaises(IntegrityError):
            Guardian.objects.create(
                name="somebody",
                address_line_1="123 main st",
                email="user@example.com",
            )

    def test_full_address(self):
        Guardian.objects.create(
            name="somebody",
            address_line_1="123 main st",
            city="Huntsville",
            state="AL",
            zip_code="36801",
            email="user@example.com",
        )
