# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.test import TestCase, Client
from django.urls import reverse, resolve
import json
# Internal:
from django.contrib.auth.models import User
from products.models import JobType, Plan
from .forms import PlanForm

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class TestPlanView(TestCase):
    @classmethod
    def setUp(self):
        """
        create test product
        """
        self.my_jobtype = JobType.objects.create(
            name='Savage',
        )
        self.my_jobtype.save()
        self.product = Plan.objects.create(
            jobtype=self.my_jobtype,
            name='',
            description='',
            price='',
        )

    def tearDown(self):
        self.plan.delete()
        self.my_jobtype.delete()

    def test_returning_the_template(self):
        response = self.client.get('/plans/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('/plans/plans.html/')


class TestPlanDetailsView(TestCase):

    @classmethod
    def setUp(self):
        """
        create test product
        """
        self.user = User.objects.create(
        )
        self.user.save()
        self.my_jobtype = JobType.objects.create(
            name='Savage',
        )
        self.my_jobtype.save()
        self.plan = Plan.objects.create(
            jobtype=self.my_jobtype,
            name='',
            description='',
            price='',
        )


    def tearDown(self):
        self.product.delete()
        self.my_jobtype.delete()


    def test_returning_the_template(self):
        response = self.client.get('/plans/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plans/plan_details.html')


class TestAddProduct(TestCase):

    def setUp(self):
        """
        create test product
        """
        self.user = User.objects.create(
            username='MyTestUser',
        )
        self.user.save()

        self.my_jobtype = JobType.objects.create(
            name='',
        )
        self.my_jobtype.save()

    def test_add_product(self):
        self.client.force_login(self.user)

        form_data = {
            'jobtype': self.jobtype,
            'name': '',
            'description': '',
            'price': '',
        }
        form = PlanForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(self.user.is_superuser)
        response = self.client.post(reverse('plans:add_plan'),
                                    data=form.data)
        self.assertEqual(response.status_code, 200)


class TestDeletePlan(TestCase):

    @classmethod
    def setUp(self):
        """
        create test product
        """
        self.user = User.objects.create(
            username='MyTestUser',
        )
        self.user.save()
        self.admin_user = User.objects.create(
            username='AdminTestUser',
        )
        self.admin_user.save()

        self.my_jobtype = JobType.objects.create(
            name='',
        )
        self.my_jobtype.save()
        self.plan = Plan.objects.create(
            category=self.my_category,
            name='',
            description='',
            price='',

        )

    def test_deleting_plan_not_admin(self):
        self.client.force_login(self.user)
        response = self.client.post('/delete/1/', follow=True)
        self.assertContains(response, 'SORRY Only site admin have  access')

    def test_deleting_plan_admin(self):
        self.client.force_login(self.admin_user)
        response = self.client.post('/delete/1/', follow=True)
        self.assertRedirects(response, reverse('plan:plans'))