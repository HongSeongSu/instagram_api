import os
import random

from django.contrib.auth import get_user_model
from django.urls import NoReverseMatch
from django.urls import resolve
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase

from post.models import Post
from utils.testcase import APITestCaseAuthMixin

User = get_user_model()


class PostTest(APITestCaseAuthMixin, APILiveServerTestCase):
    def create_post(self, num=1):

        url = reverse('api:post-list')
        for i in range(num):
            response = self.client.post(url)
            if num == 1:
                return response

    def test_apis_url_exist(self):
        try:
            resolve('/api/post/')
            resolve('/api/post/1/')
        except NoReverseMatch as e:
            self.fail(e)

    def test_post_create(self):
        # Post를 만들 유저를 생성 및 로그인
        user = self.create_user()
        self.client.login(
            username=self.test_username,
            password=self.test_password,
        )

        response = self.create_post()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('author', response.data)
        self.assertIn('created_date', response.data)

        response_author = response.data['author']
        self.assertIn('pk', response_author)
        self.assertIn('username', response_author)

        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.author.id, user.id)

    def test_cannot_post_create_not_authenticated(self):
        url = reverse('api:post-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.exists(), False)

    def test_post_list(self):

        self.create_user_and_login(self.client)

        num = random.randrange(1, 50)

        self.create_post(num)
        url = reverse('api:post-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), num)

        # 생성된 response의
        for item in response.data:
            self.assertIn('author', item)
            item_author = item['author']
            self.assertIn('pk', item_author)
            self.assertIn('username', item_author)

    def test_post_update_partial(self):
        pass

    def test_post_update(self):
        pass

    def test_post_retrieve(self):
        pass

    def test_post_destroy(self):
        pass


class PostPhotoTest(APITestCaseAuthMixin, APILiveServerTestCase):
    def test_photo_add_to_post(self):
        user = self.create_user_and_login(self.client)

        url = reverse('api:post-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.author, user)

        # 생성한 Post에 PostPhoto를 추가
        url = reverse('api:photo-create')

        # test_images.jpg파일을 이용해서 생성
        file_path = os.path.join(os.path.dirname(__file__), 'test.png')
        with open(file_path, 'rb') as fp:
            data = {
                'post': post.id,
                'photo': fp
            }
            response = self.client.post(url, data)

        # status 코드 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # key 학인
        self.assertIn('post', response.data)
        self.assertIn('photo', response.data)

        self.assertEqual(post.pk, response.data['post'])

        print(response.data)

    def test_cannot_photo_add_to_post_not_authenticated(self):
        pass

    def test_cannot_photo_add_to_post_user_is_not_author(self):
        pass
