from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        # 首先创建一个 List 实例
        list = List.objects.create()

        # 然后创建两个 Item 实例并关联到上面创建的 List 实例
        first_item = Item.objects.create(text='The first list item', list=list)
        second_item = Item.objects.create(text='Item the second', list=list)

        # 检索所有保存的 Item 实例
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        # 比较检索到的 Item 实例的文本
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


class HomePageTest(TestCase):
    # def test_displays_all_list_items(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')
    #     response = self.client.get('/')
    #     self.assertIn('itemey 1', response.content.decode())
    #     self.assertIn('itemey 2', response.content.decode())

    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    # def test_home_page_returns_correct_html(self):
    #     request = HttpRequest()#(1)
    #     response = home_page(request)#(2)
    #     html = response.content.decode('utf8')#(3)
    #     self.assertTrue(html.startswith('<html>'))#(4)
    #     self.assertIn('<title>To-Do lists</title>', html)#(5)
    #     self.assertTrue(html.endswith('</html>'))#(4)

    # def test_uses_home_template(self):
    #     response = self.client.get('/')
    #     self.assertTemplateUsed(response, 'home.html')

    # def test_only_saves_items_when_necessary(self):
    #     self.client.get('/')
    #     self.assertEqual(Item.objects.count(), 0)


def test_displays_all_list_items():
    list_user = List.objects.create()
    Item.objects.create(text='itemey 1', list=list_user)
    Item.objects.create(text='itemey 2', list=list_user)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-new-page/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        list_user = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_user)
        Item.objects.create(text='itemey 2', list=list_user)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-new-page/')
