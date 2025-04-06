from django.urls import path, re_path
from .views import (
    ContactListView,
    ContactDetailView,
    SpamReportView,
    SpamCheckView,
    SearchView,
    BulkContactImportView,
    ContactExportView
)

# For debugging
print("Loading contacts/urls.py")
print("Creating URL patterns...")

urlpatterns = [
    # Static contact endpoints (specific URLs first)
    path('contacts/import/', BulkContactImportView.as_view(), name='contact-import'),
    path('contacts/export/', ContactExportView.as_view(), name='contact-export'),
    
    # Add specific format endpoints
    path('contacts/export/csv', ContactExportView.as_view(), name='contact-export-csv'),
    path('contacts/export/json', ContactExportView.as_view(), name='contact-export-json'),
    
    # Alternative paths for export (for testing)
    path('export-contacts/', ContactExportView.as_view(), name='contact-export-alt'),
    path('export-contacts/csv', ContactExportView.as_view(), name='contact-export-alt-csv'),
    path('export-contacts/json', ContactExportView.as_view(), name='contact-export-alt-json'),
    
    path('export/', ContactExportView.as_view(), name='contact-export-simple'),
    path('export/csv', ContactExportView.as_view(), name='contact-export-simple-csv'),
    path('export/json', ContactExportView.as_view(), name='contact-export-simple-json'),
    
    # Dynamic URLs with parameters
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
    
    # Generic list endpoint
    path('contacts/', ContactListView.as_view(), name='contact-list'),
    
    # Spam endpoints
    path('spam/report/', SpamReportView.as_view(), name='spam-report'),
    path('spam/check/<str:phone_number>/', SpamCheckView.as_view(), name='spam-check'),

    # Search endpoint
    path('search/', SearchView.as_view(), name='search'),
]

# For debugging
print("URL patterns created:")
for pattern in urlpatterns:
    print(f"  - {pattern.name}: {pattern.pattern}") 