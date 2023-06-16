
from django.test import TestCase, Client
from django.urls import reverse, resolve

from django.contrib.auth.models import User
from .models import JobType, Plan



class TestTechniqueModel(TestCase):

    @classmethod
    def setUp(self):
        """
        creating and saving a new test category
        """
        self.my_jobtype = JobType().objects.create(
            name='',

        )
        self.my_jobtype.save()

    def tearDown(self):
        self.my_jobtype.delete()

    def test_get_friendly_name(self):
        self.assertTrue(self.my_jobtype.get_friendly_name())


class TestPlanModel(TestCase):

    @classmethod
    def setUp(self):
        """
        creating and saving a new test Product
        """
        self.my_jobtype = JobType.objects.create(
            name='',
        )
        self.my_jobtype.save()
        self.plan = Plan.objects.create(
            jobtype=self.my_jobtype,
            name='',
            description='',
            price='',
            
        )

    def tearDown(self):
        self.my_jobtype.delete()
        self.plan.delete()

    def test_string_method_return(self):
        self.assertEqual(str(self.plan), '')