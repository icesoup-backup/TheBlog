from django.utils.text import slugify
from django.views import generic
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Comment, Post
from .forms import CommentForm, PostForm, NewPostForm


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-createdOn')
    template_name = 'blog/index.html'
    paginate_by = 3


class PostDetail(generic.DetailView):
    template_name = 'blog/post_detail.html'
    model = Post
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = super().get_object()
        context['comments'] = obj.comments.filter(active=True)
        context['post'] = obj
        context['form'] = self.form_class
        return context


class PostEdit(LoginRequiredMixin, UpdateView):
    template_name = 'blog/post_edit.html'
    model = Post
    form_class = PostForm

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return self.object.author == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('home')
        return super(PostEdit, self).dispatch(
            request, *args, **kwargs)

    def get_success_url(self):
        print(slugify(super().get_object()))
        return reverse_lazy('post_detail',
                            kwargs={'slug': slugify(super().get_object())})


class PostNew(LoginRequiredMixin, CreateView):
    template_name = 'blog/post_new.html'
    form_class = NewPostForm
    model = Post
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user
        return initial


class PostDelete(DeleteView):
    template_name = 'blog/post_delete.html'
    model = Post
    success_url = reverse_lazy('home')

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return self.object.author == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('home')
        return super(PostDelete, self).dispatch(
            request, *args, **kwargs)


class CommentNew(CreateView):
    template_name = 'blog/post_comment.html'
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.post = self.get_post()
        self.object.name = self.request.user.username
        self.object.save()
        return super().form_valid(form)

    def get_post(self):
        return Post.objects.filter(slug=self.kwargs.get('slug')).first()

    def get_success_url(self):
        return reverse_lazy('post_detail',
                            kwargs={'slug': self.kwargs.get('slug')})
