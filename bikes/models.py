from django.db import models
from django.utils.timezone import now
from django.urls import reverse


class Make(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class Donor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    address_line_3 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return "/".join(
            str(i)
            for i in [self.name, self.email, self.phone, self.address_line_1]
            if i
        )


class Bike(models.Model):
    class BikeCondition(int, models.Choices):
        CONDITION_10 = 10, "10 (like new)"
        CONDITION_9 = 9, "9"
        CONDITION_8 = 8, "8"
        CONDITION_7 = 7, "7"
        CONDITION_6 = 6, "6"
        CONDITION_5 = 5, "5"
        CONDITION_4 = 4, "4"
        CONDITION_3 = 3, "3"
        CONDITION_2 = 2, "2"
        CONDITION_1 = 1, "1 (worst)"

    class BrakeType(models.TextChoices):
        NONE = "none"
        COASTER = "coaster"
        RIM = "rim"
        DISC = "disc"

    class BikeState(models.TextChoices):
        NEW = "new"
        NEEDS_REPAIR = "needs_repair"
        READY_FOR_SALE = "ready_for_sale"
        SOLD = "sold"
        READY_to_SCRAP = "ready_to_scrap"
        DISMANTLED = "dismantled"
        EARNED = "earned"
        ADDED_TO_FLEET = "added_to_fleet"

    class TubeFitting(models.TextChoices):
        SCHRADER = "S"
        PRESTA = "P"

    make = models.ForeignKey(Make, related_name="bikes", on_delete=models.PROTECT)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100)
    picture = models.ImageField(blank=True, null=True)
    status = models.CharField(choices=BikeState.choices, default="new", max_length=50)
    frame_size = models.CharField(max_length=20, blank=True)
    wheel_size = models.PositiveSmallIntegerField(blank=True, null=True)
    tube_fitting = models.CharField(
        max_length=1,
        choices=TubeFitting.choices,
        default="s",
    )
    brake_type = models.CharField(max_length=10, choices=BrakeType.choices)
    condition = models.PositiveSmallIntegerField(
        choices=BikeCondition.choices,
        blank=True,
        null=True,
    )
    intake_time = models.DateTimeField(default=now, blank=True, null=True)
    marked_as_needing_repair_time = models.DateTimeField(blank=True, null=True)
    marked_as_ready_for_sale_time = models.DateTimeField(blank=True, null=True)
    sold_time = models.DateTimeField(blank=True, null=True)
    marked_as_ready_for_scrap_time = models.DateTimeField(blank=True, null=True)
    dismantled_time = models.DateTimeField(blank=True, null=True)
    refurb_parts_used = models.TextField(blank=True)
    donated_by = models.ForeignKey(
        Donor,
        related_name="bikes_donated",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    notes = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse("bikes-update", kwargs={"pk": self.pk})

    def __str__(self):
        return " ".join(
            str(i) for i in [self.make, self.model, self.serial_number] if i
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("make", "serial_number"),
                name="make-serial_number",
            ),
        ]


class Repair(models.Model):
    bike = models.ForeignKey(Bike, models.PROTECT, related_name="repairs")
    user = models.ForeignKey(
        "users.User",
        models.PROTECT,
        related_name="repairs_performed",
    )
    time_started = models.DateTimeField(auto_now=False, auto_now_add=False, default=now)
    time_finished = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    action = models.TextField()
    before_picture = models.ImageField(blank=True, null=True)
    after_picture = models.ImageField(blank=True, null=True)
