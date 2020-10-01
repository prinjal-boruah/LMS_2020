
import email
import logging
import numbers
from builtins import IndexError, ValueError, object

from management.models import *
from rest_framework import serializers
from management.customencryption import *

logger = logging.getLogger(__name__)
import sys

from .models import *

from datetime import timedelta 
import datetime

class livechatleadSerializer(serializers.ModelSerializer):

    class Meta:
        model = APILead
        fields = '__all__'
  