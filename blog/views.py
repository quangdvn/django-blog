from django.db.models import query
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, View

from blog.forms import CommentForm
from blog.models import Post

# Dummy data
# posts_data = []
# Helper func
# def get_date(post):
#     return post['date']
# Create your views here.


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


def starting_page(request):

    # sorted_posts = sorted(posts_data, key=get_date, reverse=True)

    # for post in sorted_posts:
    #     print(post['slug'])
    #     print(post['date'])

    # print('***************')

    # latest_posts = sorted_posts[-3:]

    # for post in latest_posts:
    #     print(post['slug'])
    #     print(post['date'])

    # Negative index not support by Django SQL
    latest_posts = Post.objects.all().order_by('-date')[:3]

    return render(request=request,
                  template_name='blog/index.html',
                  context={
                      'posts': latest_posts
                  })


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'


def posts(request):
    all_posts = Post.objects.all().order_by('-date')

    return render(request=request,
                  template_name='blog/all-posts.html',
                  context={
                      'posts': all_posts
                  })


class PostDetailView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get('stored_posts')
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        form = CommentForm()
        post = Post.objects.get(slug=slug)

        return render(request=request,
                      template_name='blog/post-detail.html', context={
                          'post': post,
                          'comment_form': form,
                          'tags': post.tags.all(),
                          'comments': post.comments.all().order_by('-id'),
                          'is_saved_for_later': self.is_stored_post(request, post.id)
                      })

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():

            cur_comment = comment_form.save(commit=False)  # Model Form
            cur_comment.post = post
            cur_comment.save()
            print('1', cur_comment)
            return HttpResponseRedirect(reverse('post-detail', args=[slug]))
        else:
            return render(request=request,
                          template_name='blog/post-detail.html', context={
                              'post': post,
                              'comment_form': comment_form,
                              'tags': post.tags.all(),
                              'comments': post.comments.all().order_by('-id'),
                              'is_saved_for_later': self.is_stored_post(request, post.id)
                          })


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get('stored_posts')

        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context['posts'] = posts
            context['has_posts'] = True

        return render(request=request,
                      template_name='blog/stored-posts.html',
                      context=context)

    def post(self, request):
        stored_posts = request.session.get('stored_posts')

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST['post_id'])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session['stored_posts'] = stored_posts

        return HttpResponseRedirect("/")


def post_detail(request, slug):
    # Test again
    # post = next(post for post in posts_data if post['slug'] == slug)

    # post_test = [post for post in posts_data if post['slug'] == slug]

    # print(len(post_test))

    # print(post['slug'])
    # print(post['title'])

    # post = Post.objects.get(slug=slug)
    post = get_object_or_404(Post, slug=slug)

    return render(request=request,
                  template_name='blog/post-detail.html',
                  context={
                      'post': post,
                      'tags': post.tags.all()
                  })
