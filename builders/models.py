from django.db import models


# Create your models here.
class Kid(models.Model):
    user = models.OneToOneField(
        "users.User", related_name="kid", on_delete=models.CASCADE
    )
    phone_number = models.CharField(blank=True, max_length=50)
    email = models.EmailField(blank=True)
    accepts_text_messages = models.BooleanField(default=True)
    reward_bike = models.OneToOneField(
        "bikes.Bike",
        related_name="kid_earning_bike",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="kid_one_of_email_or_phone",
                check=~(models.Q(phone_number="", email="")),
            ),
        ]


class Guardian(models.Model):
    kids = models.ManyToManyField(Kid, related_name="guardians")
    name = models.CharField(max_length=100)
    phone_number = models.CharField(blank=True, max_length=50)
    accepts_text_messages = models.BooleanField(default=True)
    waiver_signed = models.BooleanField(default=False)
    email = models.EmailField(blank=True)
    address_line_1 = models.CharField(max_length=50, blank=True)
    address_line_2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                # must have at least one of email or phone
                name="guardian_email_or_phone",
                check=~(models.Q(phone_number="", email="")),
            ),
            models.CheckConstraint(
                name="all_mail_fields_blank_or_none",
                # either all email address fields are blank
                check=models.Q(
                    address_line_1="",
                    address_line_2="",
                    city="",
                    state="",
                    zip_code="",
                )  # OR
                | (  # line 1, city, state, and zip must not be blank
                    ~models.Q(address_line_1="")
                    & ~models.Q(city="")
                    & ~models.Q(state="")
                    & ~models.Q(zip_code="")
                ),
            ),
        ]
