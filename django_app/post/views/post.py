from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, DeleteView

from post.forms import PostForm
from post.models import Post, PostComment, PostPhoto

__all__ = (
    'PostList',
    'PostDetail',
    'PostCreate',
    'PostDelete',
)


class PostList(ListView):
    model = Post
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post


class PostCreate(FormView):
    template_name = 'post/post_create.html'
    form_class = PostForm
    success_url = '/post/'

    def form_valid(self, form):
        post = Post.objects.create(author=self.request.user)
        content = form.cleaned_data.get('content', '').strip()
        if content != '':
            PostComment.objects.create(post=post, author=self.request.user, content=content)
        for file in self.request.FILES.getlist('photos'):
            PostPhoto.objects.create(post=post, photo=file)
        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post:post-list')
