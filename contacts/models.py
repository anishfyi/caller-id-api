from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Contact(models.Model):
    """
    Contact model for storing user's contacts with name and phone number.
    Each contact is associated with a user (owner).
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'phone_number')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

class SpamReport(models.Model):
    """
    SpamReport model for tracking spam phone numbers.
    Each report is associated with a user who reported the number.
    """
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spam_reports')
    phone_number = PhoneNumberField()
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reporter', 'phone_number')
        ordering = ['-reported_at']

    def __str__(self):
        return f"Spam report for {self.phone_number} by {self.reporter.username}"
