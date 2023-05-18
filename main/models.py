from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from accounts.models import User
from project import settings


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.contact_form_email = settings.CONTACT_FORM_EMAIL
