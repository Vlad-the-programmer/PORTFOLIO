from rest_framework.exceptions import APIException


class NotOwner(APIException):
    status_code = 403
    default_detail = 'You cannot access a profile if you are not it\'s owner!!!'
    default_code = 'access_denied'