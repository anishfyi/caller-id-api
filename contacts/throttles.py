from rest_framework.throttling import UserRateThrottle

class ContactCreateThrottle(UserRateThrottle):
    """
    Throttle class for contact creation.
    Limits users to 2 contact creations per 10 seconds.
    """
    rate = '2/s'
    scope = 'contact_create'

class SpamReportThrottle(UserRateThrottle):
    """
    Throttle class for spam reporting.
    Limits users to 1 spam report per 10 seconds to prevent abuse.
    """
    rate = '1/s'
    scope = 'spam_report'

class SearchThrottle(UserRateThrottle):
    """
    Throttle class for search operations.
    Limits users to 30 search requests per minute.
    """
    rate = '30/m'
    scope = 'search' 