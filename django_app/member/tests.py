from django.test import LiveServerTestCase

from member.models import MyUser


class RelationTest(LiveServerTestCase):
    @staticmethod
    def create_dummy_users(num):
        return [MyUser.objects.create(username='user{}'.format(i)) for i in range(num)]
        # users =[]
        # for i in range(num):
        #     user = MyUser.objects.create(
        #         username='user{}'.format(i),
        #         password='test_password'
        #     )
        #     users.append(user)
        # return users

    def test_following(self):
        users = self.create_dummy_users(10)
        users[0].follow(users[1])
        users[0].follow(users[2])
        users[0].follow(users[3])
        users[0].follow(users[4])

        self.assertEqual(users[0].following.count(), 4)

    def test_followers(self):
        users = self.create_dummy_users(10)
        users[1].follow(users[0])
        users[2].follow(users[0])
        users[3].follow(users[0])
        users[4].follow(users[0])

        self.assertEqual(users[0].followers.count(), 4)

    def test_block_users(self):
        users = self.create_dummy_users(10)
        users[0].blocks(users[1])
        users[0].blocks(users[2])
        users[0].blocks(users[3])
        users[0].blocks(users[4])

        self.assertEqual(users[0].block_users.count(), 4)

    def test_friends(self):
        users = self.create_dummy_users(10)
        users[0].follow(users[1])
        users[0].follow(users[2])
        users[0].follow(users[3])
        users[0].follow(users[4])
        users[1].follow(users[0])
        users[2].follow(users[0])
        users[3].follow(users[0])
        users[4].follow(users[0])

        self.assertEqual(users[0].friends.count(), 4)
