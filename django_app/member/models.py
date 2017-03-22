from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    """
    1. 팔로우, 차단을 함께 만들 수 있는 중간자 모델을 구현
        검색(django follower twitter model)

    2. MyUser의
        method:
            follow: 내가 누군가를 follow 하기
            block: 내가 누군가를 block 하기
        property:
            friends: 서로 follow하고 있는 관계
            followers: 나를 follow하고 있는 User들
            followings: 내가 follow하고 있는 User들
            block_users: 내가 block한 User들
    """

    relation = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name='relation_user_set',
        through='Relationship',
    )

    def follow(self, user):
        self.relations_from_user.create(
            to_user=user,
            relation_type=Relationship.TYPE_FOLLOW
        )

    def blocks(self, user):
        self.relations_from_user.create(
            to_user=user,
            relation_type=Relationship.TYPE_BLOCK
        )

    @property
    def following(self):
        relations = self.relations_from_user.filter(
            relation_type=Relationship.TYPE_FOLLOW
        )
        return MyUser.objects.filter(id__in=relations.values('to_user_id'))

    @property
    def followers(self):
        relations = self.relations_to_user.filter(
            relation_type=Relationship.TYPE_FOLLOW
        )
        return MyUser.objects.filter(id__in=relations.values('from_user_id'))

    @property
    def block_users(self):
        relations = self.relations_from_user.filter(
            relation_type=Relationship.TYPE_BLOCK
        )
        return MyUser.objects.filter(id__in=relations.values('to_user_id'))

    @property
    def friends(self):
        return self.following & self.followers


class Relationship(models.Model):
    TYPE_FOLLOW = 'f'
    TYPE_BLOCK = 'b'

    CHOICES_RELATION_TYPE = (
        (TYPE_FOLLOW, 'Follow'),
        (TYPE_BLOCK, 'Block'),
    )
    from_user = models.ForeignKey(MyUser, related_name='relations_from_user')
    to_user = models.ForeignKey(MyUser, related_name='relations_to_user')
    relation_type = models.CharField(max_length=1, choices=CHOICES_RELATION_TYPE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Relation({}) From({}) To({})'.format(
            self.get_relation_type_display(),
            self.from_user.username,
            self.to_user.username,
        )
