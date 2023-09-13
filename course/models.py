from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    credit_hours = models.PositiveIntegerField()

    def __str__(self):
        return self.name