from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
type_choices = (
    ('bank_admin', 'Bank Admin'),
    ('branch_manager', 'Branch Manager')
)

class Profile(AbstractUser):
    user_type = models.CharField(max_length=20, choices=type_choices)
    bank = models.ForeignKey('main.Bank', on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey('main.Branch', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username