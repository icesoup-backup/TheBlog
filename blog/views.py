from django.utils.text import slugify
from django.views import generic
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from .models import Post
from .forms import CommentForm, PostForm, NewPostForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-createdOn')
    template_name = 'blog/index.html'
    paginate_by  = 3


class PostDetail(CreateView):
    template_name = 'blog/post_detail.html'
    model = Post
    form_class = CommentForm

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.request.user
        initial['post'] = self.get_object()
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = super().get_object()
        context['comments'] = obj.comments.filter(active=True)
        context['post'] = obj
        return context

    def get_success_url(self):
        print(slugify(super().get_object()))
        return reverse_lazy('post_detail', kwargs={'slug':slugify(super().get_object())})

    def comments():
        pass
    # def post(self, request, slug):
    #     template_name = 'blog/post_detail.html'
    #     post = get_object_or_404(Post, slug=slug)
    #     return render(request, template_name, {'post': post})
    #     comments = post.comments.filter(active=True)
    #     new_comment = None

    #     comment_form = CommentForm(data=request.POST)
    #     if comment_form.is_valid():
    #         new_comment = comment_form.save(commit=False)
    #         new_comment.post = post
    #         new_comment.save()
    #     return render(request, template_name, {'post': post,
    #                                            'comments': comments,
    #                                            'new_comment': new_comment,
    #                                            'comment_form': comment_form})

    # def get(self, request, slug):
    #     template_name = 'blog/post_detail.html'
    #     post = get_object_or_404(Post, slug=slug)
    #     comments = post.comments.filter(active=True)
    #     comment_form = CommentForm(initial={'name': request.user})

    #     return render(request, template_name, {'post': post,
    #                                            'comments': comments,
    #                                            'comment_form': comment_form})


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
        return reverse_lazy('post_detail', kwargs={'slug':slugify(super().get_object())})    


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


# class CommentNew(CreateView):
#     template_name = 'blog/post_detail.html'
#     model = Post
#     form_class = CommentForm

#     def get_initial(self):
#         initial = super().get_initial()
#         initial['name'] = self.request.user
#         initial['post'] = self.get_object()
#         return initial
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         obj = super().get_object()
#         context['comments'] = obj.comments.filter(active=True)
#         context['post'] = obj
#         return context

#     def get_success_url(self):
#         print(slugify(super().get_object()))
#         return reverse_lazy('post_detail', kwargs={'slug':slugify(super().get_object())})