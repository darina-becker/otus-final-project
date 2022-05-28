from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django.views.generic.detail import SingleObjectMixin

from account.mixins import IsDeveloperMixin
from developer.models import DevAccount
from .forms import AppCreateForm, CommentForm, RatingForm
from .models import App, Comment, Rating


def index(request):
    # all_apps = App.objects.prefetch_related().all()
    # context = {
    #     'all_apps': all_apps
    # }
    return render(request, 'app/index.html')


@login_required
def download(request, pk):
    app = App.objects.get(pk=pk)
    url = app.apkfile.url
    App.objects.filter(pk=pk).update(download_counter=app.download_counter + 1)
    return HttpResponseRedirect(redirect_to=url)


class AppDisplay(DetailView):
    model = App

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_pk = context.get('app').pk
        user_pk = context.get('view').request.user.pk
        comm_exist = Comment.objects.filter(app=app_pk).filter(user=user_pk).first()
        if comm_exist is None:
            context['cform'] = CommentForm()
        rate_exist = Rating.objects.filter(app=app_pk).filter(user=user_pk).first()
        if rate_exist is None:
            context['rform'] = RatingForm()
        return context


class AppDetailView(DetailView):
    model = App
    page_title = 'App Name'

    def get(self, request, *args, **kwargs):
        view = AppDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = None
        rate = request.POST.get('rate', None)
        comment = request.POST.get('comment', None)
        if rate is not None:
            view = AppRating.as_view()
        elif comment is not None:
            view = AppComment.as_view()
        return view(request, *args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('app-detail', args=[str(self.pk)])


class AppListView(LoginRequiredMixin, ListView):
    model = App
    paginate_by = 20


class AuthorAppListView(IsDeveloperMixin, ListView):
    model = App
    template_name = 'app/app_list.html'

    def get_queryset(self):
        self.author = get_object_or_404(DevAccount, user=self.request.user.pk)
        return App.objects.filter(author=self.author)


class AppCreateView(LoginRequiredMixin, IsDeveloperMixin, CreateView):
    model = App
    success_url = reverse_lazy('main')
    form_class = AppCreateForm

    def get_form_kwargs(self):
        kwargs = super(AppCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        app_form = form.save(commit=False)
        app_form.author_id = self.request.user.pk
        app_form.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(viewname='devs:dev_main')


class AppUpdateView(UpdateView):
    model = App
    success_url = reverse_lazy('app.detail')
    fields = ['desc', 'last_update']


class AppComment(SingleObjectMixin, FormView):
    model = App
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AppComment, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.app = self.object
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        app = self.get_object()
        return reverse(viewname='apps:detail', kwargs={'pk': app.pk}) + '#comments'


class AppRating(SingleObjectMixin, FormView):
    model = App
    form_class = RatingForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AppRating, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        rate = form.save(commit=False)
        rate.app = self.object
        rate.user = self.request.user
        rate.save()
        return super().form_valid(form)

    def get_success_url(self):
        app = self.get_object()
        return reverse(viewname='apps:detail', kwargs={'pk': app.pk})
