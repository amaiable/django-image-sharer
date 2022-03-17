from django.views.generic import TemplateView, DetailView, FormView
from django.contrib import messages

from .forms import PostForm
from .models import Post

# Use class based view


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all().order_by("-id")
        return context


class PostDetailView(DetailView):
    template_name = "detail.html"
    model = Post


class AddPostView(FormView):
    template_name = "new_post.html"
    form_class = PostForm
    success_url = "/"  # Goes back to home page

    def dispatch(self, request, *args, **kwargs):
        # Just using the fact that dispatch exists so we can get our requests variable
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Create a new post
        new_object = Post.objects.create(
            text=form.cleaned_data["text"],
            image=form.cleaned_data["image"]
        )
        messages.add_message(self.request, messages.SUCCESS,
                             "Your post was successful")
        return super().form_valid(form)
