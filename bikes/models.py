from django.db import models
from django.utils.timezone import now


class Make(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class Bike(models.Model):
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
        max_length=1, choices=TubeFitting.choices, default="s"
    )
    brake_type = models.CharField(max_length=10, choices=BrakeType.choices)

    def __str__(self):
        return " ".join(
            str(i) for i in [self.make, self.model, self.serial_number] if i
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("make", "serial_number"), name="make-serial_number"
            ),
        ]


class Repair(models.Model):
    bike = models.ForeignKey(Bike, models.PROTECT, related_name="repairs")
    user = models.ForeignKey(
        "users.User", models.PROTECT, related_name="repairs_performed"
    )
    time_started = models.DateTimeField(auto_now=False, auto_now_add=False, default=now)
    time_finished = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    action = models.TextField()
    before_picture = models.ImageField(blank=True, null=True)
    after_picture = models.ImageField(blank=True, null=True)
