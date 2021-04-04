from django.test import TestCase
from notes.models import User, StudyGroup, Category
from django.urls import reverse
from faker import Faker

fake = Faker()

# Create your tests here.

def add_category(name="Economics"):
    category = Category.objects.get_or_create(categoryName=name)[0]
    category.save()
    return category

testCategory = add_category()

def add_user(username="test", email="test@gmail.com"):
    user = User.objects.get_or_create(username=username)[0]
    user.email = email
    user.set_password("test")
    user.save()
    return user

testUser = add_user()

def add_studyGroup(admin=testUser, cat=testCategory, name="test Group", members=[]):
    group = StudyGroup.objects.get_or_create(category=cat, groupName=name, admin=admin)[0]
    group.description = "test description"
    group.rules = "test rules"
    
    for member in members:
        group.members.add(member)

    group.save()
    return group

testGroup = add_studyGroup()

class studyGorupTests(TestCase):
    def test_slug_group_creation(self):
        self.assertEqual((testGroup.slug == "test-group"), True)
      
class searchViewTests(TestCase):
    def test_correct_account(self):
        response = self.client.get(reverse('notes:search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'search')

class RemoveNoteViewTests(TestCase):
    def test_cannot_remove_note_by_only_visiting_url(self):
        response = self.client.get(reverse('notes:remove_note'))
        self.assertEqual(response.status_code, 302)

class AddLinkViewTests(TestCase):
    def test_cannot_access_addNote_by_only_visiting_url(self):
        response = self.client.get(reverse('notes:add_link', kwargs={'group_slug':"test-group"}))
        self.assertEqual(response.status_code, 302)
        