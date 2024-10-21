from rest_framework.throttling import UserRateThrottle


class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'
    
class ReviewListThottle(UserRateThrottle):
    scope = 'review-list'