import json
import pathlib
import unittest

import pytest
import responses
from django.core.management import call_command
from freezegun import freeze_time


root = pathlib.Path(__file__).parent


