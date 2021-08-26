from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from .models import Post
from .forms import CommentForm, PostForm, NewPostForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-createdOn')
    template_name = 'blog/index.html'


class PostDetail(generic.DetailView):
    def post(self, request, slug):
        template_name = 'blog/post_detail.html'
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(active=True)
        new_comment = None

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
        return render(request, template_name, {'post': post,
                                               'comments': comments,
                                               'new_comment': new_comment,
                                               'comment_form': comment_form})

    def get(self, request, slug):
        template_name = 'blog/post_detail.html'
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(active=True)
        comment_form = CommentForm(initial={'name':request.user})

        return render(request, template_name, {'post': post,
                                               'comments': comments,
                                               'comment_form': comment_form})


class PostEdit(LoginRequiredMixin, UpdateView):
    template_name = 'blog/post_edit.html'
    model = Post
    form_class = PostForm
    success_url = 'post_detail'
    


""" class PostEdit(generic.DetailView):
    def get(self, request, slug):
        template_name = 'blog/post_edit.html'
        post_obj = get_object_or_404(Post, slug=slug)
        values = {
            'content': post_obj.content
        }
        post_form = PostForm(initial=values)
        # print(post_form)
        return render(request, template_name, {'post_form': post_form})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        post_form = PostForm(data=request.POST)
        if(post_form.is_valid):
            post.content = post_form.data.get('content')
            post.save()
        return redirect('home')
        # return render(request, template_name, {'post_form':post_form}) """


class PostNew(CreateView):
    if User.is_authenticated:
        template_name = 'blog/post_new.html'
        form_class = NewPostForm
        model = Post
        success_url = '/'
    else:
        redirect('home')

    def get_initial(self):
        initial =  super().get_initial()
        initial['author'] = self.request.user
        return initial


# class PostNew(generic.DetailView):
#     def get(self, request):
#         template_name = 'blog/post_new.html'
#         post_form = NewPostForm(initial={'author':request.user.id})
#         print(post_form)
#         return render(request, template_name, {'post_form':post_form})

#     def post(self, request):
#         template_name = 'blog/post_new.html'
#         post_form = NewPostForm(data=request.POST)
#         if post_form.is_valid:
#             print(post_form)
#             post_form.save()
#             return redirect('home')
#         else:
#             return render(request, template_name, {'post_form':post_form})

class PostDelete(DeleteView):
    template_name = 'blog/post_delete.html'
    model = Post
    success_url = '/'