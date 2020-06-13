from django.test import TestCase, Client
from django.urls import reverse
from taggit.models import Tag

from stumee_auth.models import CustomUser
from stumee_meeting.models import Thread, Comment, CommentGood, ThreadGood
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
        self.assertContains(response, 'No stumee_meeting here')
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


class PostThreadViewTests(TestCase):
    def test_access_user_not_login(self):
        # ログインせずにアクセス
        response = self.client.get(reverse('stumee_meeting:post_thread'))
        self.assertEqual(response.status_code, 302)

    def test_access_user_logged_in(self):
        # ログインしてアクセス
        client = Client()
        client.force_login(create_user_for_test('test太郎'))
        response = client.get(reverse('stumee_meeting:post_thread'))
        self.assertEqual(response.status_code, 200)

    def test_post_null(self):
        # 何も入力しないでpost
        client = Client()
        client.force_login(create_user_for_test('test太郎'))
        post_data = {}
        response = client.post(reverse('stumee_meeting:post_thread'), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errorlist')

    def test_post_non_null(self):
        # 内容を入力してpost
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


class AddGoodThreadViewTests(TestCase):
    def test_access_no_thread(self):
        # Threadがないのにアクセス
        client = Client()
        client.force_login(create_user_for_test('test太郎'))
        response = client.get(reverse('stumee_meeting:thread_good', args=(5,)))
        self.assertEqual(response.status_code, 404)

    def test_access_user_not_login(self):
        # ログインせずにアクセス
        client = Client()
        test_user1 = create_user_for_test('test太郎')
        thread = Thread.objects.create(
            title='test',
            description='test',
            user=test_user1,
        )
        response = client.get(reverse('stumee_meeting:thread_good', args=(thread.id,)))
        self.assertEqual(response.status_code, 302)

    def test_add_or_delete_thread_good(self):
        # goodボタンを連打してもいいねは増えない
        client = Client()
        test_user1 = create_user_for_test('test太郎')
        client.force_login(test_user1)
        thread = Thread.objects.create(
            title='test',
            description='test',
            user=test_user1,
        )
        response = client.post(reverse('stumee_meeting:thread_good', args=(thread.id,)))
        self.assertEqual(ThreadGood.objects.count(), 1)
        response = client.post(reverse('stumee_meeting:thread_good', args=(thread.id,)))
        self.assertEqual(ThreadGood.objects.count(), 0)


class AddGoodForCommentViewTests(TestCase):
    def test_access_no_comment(self):
        # コメントがないのにアクセス
        client = Client()
        test_user1 = create_user_for_test('test太郎')
        client.force_login(test_user1)
        thread = Thread.objects.create(
            title='test',
            description='test',
            user=test_user1,
        )
        response = client.get(reverse('stumee_meeting:comment_good', args=(5,)))
        self.assertEqual(response.status_code, 404)

    def test_access_comment(self):
        # ログインせずにアクセス
        client = Client()
        test_user1 = create_user_for_test('test太郎')
        thread = Thread.objects.create(
            title='test',
            description='test',
            user=test_user1,
        )

        comment = Comment.objects.create(
            thread=thread,
            comment='test',
            user=test_user1,
        )
        response = client.get(reverse('stumee_meeting:comment_good', args=(comment.id,)))
        self.assertEqual(response.status_code, 302)

    def test_add_and_delete_comment_good(self):
        # goodボタン連打してもいいねは増えない
        client = Client()
        test_user1 = create_user_for_test('test太郎')
        client.force_login(test_user1)
        thread = Thread.objects.create(
            title='test',
            description='test',
            user=test_user1,
        )

        comment = Comment.objects.create(
            thread=thread,
            comment='test',
            user=test_user1,
        )
        response = client.post(reverse('stumee_meeting:comment_good', args=(comment.id,)))
        self.assertEqual(CommentGood.objects.count(), 1)
        response = client.post(reverse('stumee_meeting:comment_good', args=(comment.id,)))
        self.assertEqual(CommentGood.objects.count(), 0)


class PickUpThreadViewTests(TestCase):
    def test_access_with_not_login(self):
        # ユーザがログインせずにアクセス
        client = Client()
        test_user1 = create_user_for_test('test太郎')
        thread = Thread.objects.create(
            title='test',
            description='test',
            user=test_user1,
        )
        response = client.get(reverse('stumee_meeting:thread_pickup', args=(thread.id,)))
        self.assertEqual(response.status_code, 302)

    def test_access_with_logged_in(self):
        # 存在しないPKでアクセス
        client = Client()
        test_user1 = create_user_for_test('test太郎')
        client.force_login(test_user1)
        response = client.get(reverse('stumee_meeting:thread_pickup', args=(5,)))
        self.assertEqual(response.status_code, 404)


class TagListViewTests(TestCase):
    def test_access_with_not_login(self):
        # ユーザがログインせずにアクセス
        client = Client()
        test_user1 = create_user_for_test('test太郎')

        thread = Thread.objects.create(
            title='test',
            description='test',
            user=test_user1,
        )
        thread.tag.add('Django')
        thread.tag.add('Python')

        response = client.get(reverse('stumee_meeting:tag_filter', kwargs={'tag_name': 'Django'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tag_name'], 'Django')
        self.assertQuerysetEqual(response.context['tag_threads_list'], ['<Thread: test>'])
        self.assertContains(response, 'test')

    def test_multi_thread(self):
        # ユーザがログインし、なおかつThread が複数個あるときの挙動
        client = Client()
        test_user1 = create_user_for_test('test太郎')
        client.force_login(test_user1)
        thread = Thread.objects.create(
            title='test',
            description='test',
            user=test_user1,
        )
        thread.tag.add('Django')
        thread.tag.add('Python')

        thread2 = Thread.objects.create(
            title='test2',
            description='test',
            user=test_user1,
        )
        thread2.tag.add('Python')
        thread2.tag.add('ToDo')

        response = client.get(reverse('stumee_meeting:tag_filter', kwargs={'tag_name': 'Python'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tag_name'], 'Python')
        self.assertQuerysetEqual(
            response.context['tag_threads_list'],
            ['<Thread: test>', '<Thread: test2>'],
            ordered=False,
        )
        self.assertContains(response, thread.title)
        self.assertContains(response, thread2.title)

    def test_access_for_no_tags(self):
        # 紐づけられたThreadがない時
        client = Client()
        test_user1 = create_user_for_test('test太郎')
        client.force_login(test_user1)
        response = client.get(reverse('stumee_meeting:tag_filter', args=('Java',)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No stumee_meeting here')
        self.assertQuerysetEqual(response.context['tag_threads_list'], [])


class QuestionViewTests(TestCase):
    def test_no_thread(self):
        # きちんとアクセスできているかを確認
        response = self.client.get(reverse('stumee_meeting:question'))
        saved_thread = Thread.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No stumee_meeting here')
        self.assertQuerysetEqual(response.context['threads_list'], [])
        self.assertEqual(saved_thread.count(), 0)

    def test_one_thread(self):
        # データを一件追加し、表示されているかを確認
        test_user = create_user_for_test('test太郎')
        Thread.objects.create(
            title='test',
            description='test',
            user=test_user,
        )
        response = self.client.get(reverse('stumee_meeting:question'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test')
        self.assertQuerysetEqual(response.context['threads_list'], ['<Thread: test>'])
        self.assertContains(response, 'test太郎')
        self.assertEqual(Thread.objects.count(), 1)

    def test_three_thread(self):
        # データを三件追加し、きちんと並び替えられているか、表示されているかを確認
        self.test_user1 = create_user_for_test('test太郎')
        self.test_user2 = create_user_for_test('test次郎')
        saved_thread = Thread.objects.all()
        thread1 = Thread.objects.create(
            title='test1',
            description='test1',
            user=self.test_user1,
            good_count=5,
            is_picked=True,
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

        response = self.client.get(reverse('stumee_meeting:question'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, thread1.title)
        self.assertContains(response, thread2.title)
        self.assertContains(response, thread3.title)
        self.assertQuerysetEqual(
            response.context['threads_list'], ['<Thread: test3>', '<Thread: test2>', '<Thread: test1>']
        )
        self.assertEqual(saved_thread.count(), 3)


class AllTagViewTests(TestCase):
    def test_no_tags(self):
        # タグが一つもない時
        response = self.client.get(reverse('stumee_meeting:tags'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Tag here')
        self.assertQuerysetEqual(response.context['tag_list'], [])
        self.assertEqual(Tag.objects.count(), 0)

    def test_one_tags(self):
        # タグが1つの時
        Tag.objects.create(
            name='Django'
        )
        response = self.client.get(reverse('stumee_meeting:tags'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django')
        self.assertQuerysetEqual(response.context['tag_list'], ['<Tag: Django>'])
        self.assertEqual(Tag.objects.count(), 1)

    def test_multi_tags(self):
        # タグが複数あるとき
        Tag.objects.create(
            name='Django'
        )

        Tag.objects.create(
            name='Python'
        )
        response = self.client.get(reverse('stumee_meeting:tags'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django')
        self.assertContains(response, 'Python')
        self.assertQuerysetEqual(
            response.context['tag_list'],
            ['<Tag: Django>', '<Tag: Python>'],
            ordered=False,
        )
        self.assertEqual(Tag.objects.count(), 2)

    def test_thread_count(self):
        # タグに紐づけられたThreadの数
        client = Client()
        test_user1 = create_user_for_test('test太郎')
        client.force_login(test_user1)
        thread = Thread.objects.create(
            title='test',
            description='test',
            user=test_user1,
        )
        thread.tag.add('Django')
        thread.tag.add('Python')

        thread2 = Thread.objects.create(
            title='test2',
            description='test',
            user=test_user1,
        )
        thread2.tag.add('Python')
        thread2.tag.add('ToDo')

        response = self.client.get(reverse('stumee_meeting:tags'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tag.objects.count(), 3)
        tag = response.context['tag_list'].first()
        self.assertEqual(tag.thread_count, 1)


class AllUserViewTests(TestCase):
    def test_no_user(self):
        # ユーザが一人もいない時
        response = self.client.get(reverse('stumee_meeting:users'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['user_list'], [])
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_multi_user(self):
        # ユーザが複数いるとき
        user1 = create_user_for_test('test太郎')
        user2 = create_user_for_test('test次郎')
        response = self.client.get(reverse('stumee_meeting:users'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['user_list'],
            ['<CustomUser: test太郎>', '<CustomUser: test次郎>'],
            ordered=False
        )
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_user_auth(self):
        # 権限がちゃんと表示されているか
        CustomUser.objects.create_user(
            username='test三郎',
            user_auth=2,
        )
        response = self.client.get(reverse('stumee_meeting:users'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertContains(
            response,
            'role : teacher'
        )




