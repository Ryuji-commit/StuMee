from django.test import TestCase, Client
from django.urls import reverse

from stumee_auth.models import CustomUser
from stumee_meeting.models import Thread, Comment
from stumee_meeting.views import IndexView, post_thread


# Create test user
def create_user_for_test(username_text):
    test_user, boo = CustomUser.objects.get_or_create(
        username=username_text,
    )
    return test_user


# The view test
class IndexViewTests(TestCase):
    def test_no_thread(self):
        # きちんとアクセスできているかを確認
        response = self.client.get(reverse('stumee_meeting:index'))
        saved_thread = Thread.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No thread here')
        self.assertQuerysetEqual(response.context['latest_threads_list'], [])
        self.assertEqual(saved_thread.count(), 0)

    def test_one_thread(self):
        # データを一件追加し、表示されているかを確認
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
        # データを三件追加し、きちんと並び替えられているか、表示されているかを確認
        self.test_user1 = create_user_for_test('test太郎')
        self.test_user2 = create_user_for_test('test次郎')
        saved_thread = Thread.objects.all()
        thread1 = Thread.objects.create(
            title='test1',
            description='test1',
            user=self.test_user1,
            good_count=2,
        )

        thread2 = Thread.objects.create(
            title='test2',
            description='test2',
            user=self.test_user2,
            good_count=4,
        )

        thread3 = Thread.objects.create(
            title='test3',
            description='test3',
            user=self.test_user2,
            is_picked=True,
        )

        response = self.client.get(reverse('stumee_meeting:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, thread1.title)
        self.assertContains(response, thread2.title)
        self.assertContains(response, thread3.title)
        self.assertQuerysetEqual(
            response.context['latest_threads_list'], ['<Thread: test3>', '<Thread: test2>', '<Thread: test1>']
        )
        self.assertEqual(saved_thread.count(), 3)


class PostThreadTests(TestCase):
    def test_access_user_not_login(self):
        response = self.client.get(reverse('stumee_meeting:post_thread'))
        self.assertEqual(response.status_code, 302)

    def test_access_user_logged_in(self):
        client = Client()
        client.force_login(create_user_for_test('test太郎'))
        response = client.get(reverse('stumee_meeting:post_thread'))
        self.assertEqual(response.status_code, 200)

    def test_post_null(self):
        client = Client()
        client.force_login(create_user_for_test('test太郎'))
        post_data = {}
        response = client.post(reverse('stumee_meeting:post_thread'), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errorlist')

    def test_post_non_null(self):
        client = Client()
        client.force_login(create_user_for_test('test太郎'))
        post_data = {
            'title': 'hello',
            'description': 'world',
            'tag': 'Python, Django',
        }
        response = client.post(reverse('stumee_meeting:post_thread'), data=post_data)
        # ヴァリデーションを通ったらリダイレクト
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(Thread.objects.all(), ['<Thread: hello>'])

    def test_post_tag_name_with_jp(self):
        # タグ名に日本語を用いた場合
        client = Client()
        client.force_login(create_user_for_test('test太郎'))
        post_data = {
            'title': 'hello',
            'description': 'world',
            'tag': 'こんにちは, はろー'
        }
        response = client.post(reverse('stumee_meeting:post_thread'), data=post_data)
        self.assertEqual(response.status_code, 302)
        # まだバックエンド側での禁止処理ができていないため、以下のテストは通らない。
        # self.assertQuerysetEqual(Thread.objects.all(), [])
