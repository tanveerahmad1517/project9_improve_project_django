import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_webtest import WebTest


from . import forms
from . import models


class ViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='vasilty',
            email='vasilty@example.com',
            password='password',
        )

        self.ingredient1 = models.Ingredient.objects.create(name='Chocolate')
        self.ingredient2 = models.Ingredient.objects.create(name='Coconut')
        self.ingredient3 = models.Ingredient.objects.create(name='Vanilla')

        self.item1 = models.Item.objects.create(
            name='Chocolate-Vanilla',
            description='The best Chocolate-Vanilla dessert in the world.',
            chef=self.user1,
        )
        self.item2 = models.Item.objects.create(
            name='Coconut-Vanilla',
            description='You will never forget our Coconut-Vanilla '
                        'masterpiece.',
            chef=self.user1,
        )

        self.menu1 = models.Menu.objects.create(
            season='July2016',
        )

        self.menu2 = models.Menu.objects.create(
            season='August2016',
            expiration_date=datetime.date(2016, 9, 1)
        )

        self.item1.ingredients = [self.ingredient1, self.ingredient3]
        self.item1.items = [self.menu1, self.menu2]
        self.item1.save()

        self.menu1.items = [self.item1]
        self.menu1.save()

        self.item2.ingredients = [self.ingredient2, self.ingredient3]
        self.item2.items = [self.menu2]
        self.item2.save()

        self.menu2.items = [self.item1, self.item2]
        self.menu2.save()

    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu1, resp.context['menus'])
        self.assertIn(self.menu2, resp.context['menus'])
        self.assertContains(resp, self.menu1.season)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu:detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu1, resp.context['menu'])
        self.assertContains(resp, self.menu1.season)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

        resp = self.client.get(reverse('menu:detail', kwargs={'pk': 4}))
        self.assertEqual(resp.status_code, 404)

    def test_item_detail_view(self):
        resp = self.client.get(reverse('menu:item_detail', kwargs={'pk': 2}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.item2, resp.context['item'])
        self.assertContains(resp, self.item2.name)
        self.assertTemplateUsed(resp, 'menu/detail_item.html')

        resp = self.client.get(reverse('menu:item_detail', kwargs={'pk': 3}))
        self.assertEqual(resp.status_code, 404)


class FormViewTest(WebTest):
    def setUp(self):
        ViewTests.setUp(self)

    def test_view_page(self):
        page = self.app.get(reverse('menu:new'))
        self.assertEqual(len(page.forms), 1)

    def test_form_error(self):
        page = self.app.get(reverse('menu:new'))
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_new_form_success(self):
        page = self.app.get(reverse('menu:new'))
        page.form['season'] = 'May2020'
        page.form['items'] = [1, 2]
        page.form['expiration_date_month'] = 7
        page.form['expiration_date_day'] = 11
        page.form['expiration_date_year'] = 2020
        page.form.submit()
        self.assertTrue(models.Menu.objects.filter(pk=3).exists())

    def test_edit_form_success(self):
        page = self.app.get(reverse('menu:edit', kwargs={'pk': self.menu1.pk}))
        page.form['season'] = 'May2017'
        page.form['items'] = [1]
        page.form['expiration_date_month'] = 7
        page.form['expiration_date_day'] = 11
        page.form['expiration_date_year'] = 2017
        page = page.form.submit()
        self.assertRedirects(page, reverse('menu:detail',
                                           kwargs={'pk': self.menu1.pk}))
        self.assertEqual(len(self.menu1.items.all()), 1)
        self.assertIn(self.item1, self.menu1.items.all())


class FormTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='vasilty',
            email='vasilty@example.com',
            password='password',
        )

        self.item1 = models.Item.objects.create(
            name='Chocolate-Vanilla',
            description='The best Chocolate-Vanilla dessert in the world.',
            chef=self.user1,
        )
        self.item2 = models.Item.objects.create(
            name='Coconut-Vanilla',
            description='You will never forget our Coconut-Vanilla '
                        'masterpiece.',
            chef=self.user1,
        )

    def test_menu_form_valid(self):
        form = forms.MenuForm({
            'season': 'May2017',
            'items': [1],
            'expiration_date': datetime.datetime.now().date(),
        })
        self.assertTrue(form.is_valid())

    def test_menu_form_blank(self):
        form = forms.MenuForm({
            'season': '',
            'items': [],
            'expiration_date': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'season': ['This field is required.'],
            'items': ['This field is required.'],
        })

    def test_menu_form_expiration_date(self):
        form = forms.MenuForm({
            'season': 'May2017',
            'items': [1],
            'expiration_date': datetime.date(1999, 1, 1),
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'expiration_date': ['Expiration date must be in the future.'],
        })
