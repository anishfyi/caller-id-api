from rest_framework import serializers
from .models import Contact, SpamReport
from django.contrib.auth import get_user_model
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.serializerfields import PhoneNumberField

User = get_user_model()

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Contact model.
    Handles contact creation and updates with phone number validation.
    """
    phone_number = PhoneNumberField()

    class Meta:
        model = Contact
        fields = ('id', 'name', 'phone_number', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def to_representation(self, instance):
        """
        Convert phone number to string in response.
        """
        ret = super().to_representation(instance)
        ret['phone_number'] = str(ret['phone_number'])
        return ret

class SpamReportSerializer(serializers.ModelSerializer):
    """
    Serializer for SpamReport model.
    Handles spam report creation with phone number validation.
    """
    phone_number = PhoneNumberField()
    reporter_name = serializers.SerializerMethodField()

    class Meta:
        model = SpamReport
        fields = ('id', 'phone_number', 'reported_at', 'reporter_name')
        read_only_fields = ('reported_at', 'reporter_name')

    def get_reporter_name(self, obj):
        return obj.reporter.get_full_name() if obj.reporter else ""

    def to_representation(self, instance):
        """
        Convert phone number to string in response.
        """
        ret = super().to_representation(instance)
        ret['phone_number'] = str(ret['phone_number'])
        return ret

class SearchResultSerializer(serializers.Serializer):
    """
    Serializer for search results that can handle both User and Contact objects
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.SerializerMethodField()
    is_registered = serializers.BooleanField()
    spam_likelihood = serializers.FloatField()

    def get_email(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None

        # For registered users, show email only if the requesting user is in their contacts
        if obj['is_registered']:
            return obj['email'] if Contact.objects.filter(
                owner=request.user,
                phone_number=obj['phone_number']
            ).exists() else None

        # For contacts, show email only if the requesting user owns the contact
        return obj['email'] if Contact.objects.filter(
            owner=request.user,
            phone_number=obj['phone_number']
        ).exists() else None

    def get_phone_number(self, obj):
        # Handle both model instances and dictionary items
        if isinstance(obj, dict):
            return obj['phone_number']
        elif isinstance(obj, User):
            return str(obj.profile.phone_number)
        return str(obj.phone_number)

    def get_spam_likelihood(self, obj):
        phone_number = self.get_phone_number(obj)
        try:
            phone_obj = PhoneNumber.from_string(phone_number)
            
            # Count spam reports
            spam_count = SpamReport.objects.filter(phone_number=phone_obj).count()
            # Count contacts (non-spam)
            contact_count = Contact.objects.filter(phone_number=phone_obj).count()
            
            total_references = spam_count + contact_count
            if total_references == 0:
                return 0
                
            return round((spam_count / total_references) * 100, 2)
        except:
            return 0 