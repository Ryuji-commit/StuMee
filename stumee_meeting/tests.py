from django.test import TestCase, Client
from django.urls import reverse

from stumee_auth.models import CustomUser
from .models import Thread, Comment
from .views import IndexView, post_thread


# Create your tests here.
def create_user_for_test(username_text):
    test_user, boo = CustomUser.objects.get_or_create(
        username=username_text,
    )
    return test_user


class IndexViewTests(TestCase):
    def test_no_thread(self):
        response = self.client.get(reverse('stumee_meeting:index'))
        saved_thread = Thread.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No thread here')
        self.assertQuerysetEqual(response.context['latest_threads_list'], [])
        self.assertEqual(saved_thread.count(), 0)

    def test_one_thread(self):
        self.test_user = create_user_for_test('test太郎')
        saved_thread = Thread.objects.all()
        Thread.objects.create(
            title='test',
            description='test',
            user=self.test_user,
        )
        response = self.client.get(reverse('stumee_meeting:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test')
        self.assertQuerysetEqual(response.context['latest_threads_list'], ['<Thread: test>'])
        self.assertContains(response, 'test太郎')
        self.assertEqual(saved_thread.count(), 1)

    def test_three_thread(self):
        self.test_user1 = create_user_for_test('test太郎')
        self.test_user2 = create_user_for_test('test次郎')
        saved_thread = Thread.objects.all()
        Thread.objects.create(
            title='test1',
            description='test1',
            user=self.test_user1,
            good_count=2,
        )

        Thread.objects.create(
            title='test2',
            description='test2',
            user=self.test_user2,
            good_count=4,
        )

        Thread.objects.create(
            title='test3',
            description='test3',
            user=self.test_user2,
            is_picked=True,
        )

        response = self.client.get(reverse('stumee_meeting:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test2')
        self.assertQuerysetEqual(
            response.context['latest_threads_list'], ['<Thread: test3>', '<Thread: test2>', '<Thread: test1>']
        )
        self.assertEqual(saved_thread.count(), 3)





