from behave import fixture, use_fixture
from django.test import RequestFactory
from django.test.runner import DiscoverRunner
import sys
import os
from django import setup
from django.urls import reverse
from django.test import RequestFactory
from django.conf import settings

def before_all(context):
    settings.DEBUG = False
    context.factory = RequestFactory()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if project_root not in sys.path:
    sys.path.append(project_root)

os.environ['DJANGO_SETTINGS_MODULE'] = 'solo_assessment.settings'
setup()

@fixture
def django_test_runner(context):
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    context.request_factory = RequestFactory()
    yield
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()

def before_all(context):
    use_fixture(django_test_runner, context)