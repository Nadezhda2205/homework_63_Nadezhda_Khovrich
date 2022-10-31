from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q


from accounts.forms import CustomUserСreationForm
from accounts.forms import LoginForm
from accounts.models import Account



class LoginView(TemplateView):
    template_name = 'accounts/login.html'
    form = LoginForm


    def get(self, request, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            return redirect('login')

        username: str = form.cleaned_data.get('username')
        password: str = form.cleaned_data.get('password')
        user = authenticate(request=request, username=username, password=password)

        if not user:
            return redirect('login')

        login(request, user)

        return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('login')


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserСreationForm
    succes_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        context = {}
        context['form'] = form
        return self.render_to_response(context)


class AccountDetailView(DetailView):
    template_name = 'accounts/account_detail.html'
    model = Account
    context_object_name = 'account'

    def get_object(self, queryset=None):
        return get_object_or_404(Account, username=self.kwargs.get('slug'))
        

def unsubscribe_view(request: WSGIRequest, slug):
    user_from_request: Account = request.user
    user_by_slug = get_object_or_404(Account, username=slug)
    user_from_request.subscriptions.remove(user_by_slug)
    return redirect ('account_detail', slug=slug)

def subscribe_view(request: WSGIRequest, slug):
    user_from_request: Account = request.user
    user_by_slug = get_object_or_404(Account, username=slug)
    user_from_request.subscriptions.add(user_by_slug)
    return redirect ('account_detail', slug=slug)


class SearchAccountListView(ListView):
    template_name: str = 'account_list.html'
    model = Account
    context_object_name = 'accounts'
 
    def get(self, request, *args, **kwargs):
        self.search_value = request.GET.get('search')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(first_name__iregex=self.search_value) | Q(email__iregex=self.search_value) | Q(username__iregex=self.search_value)
                )
        return queryset

