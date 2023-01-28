from ads.models import Article,Fav
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from ads.forms import CreateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.db.models import Q


class ArticleListView(OwnerListView):
    model = Article
    # By convention:
    template_name = "ads/article_list.html"
    
    def get(self, request) :
        strval =  request.GET.get("search", False)
        
        if strval :
            # Simple title-only search
            # __icontains for case-insensitive search
            strval=strval.strip()
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            query.add(Q(tags__name__in=[strval]), Q.OR)
            thing_list = Article.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]
        else :
            thing_list = Article.objects.all().order_by('-updated_at')[:10]        
        #thing_list = Article.objects.all() if there is no search
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        ctx = {'article_list' : thing_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)

class ArticleDetailView(OwnerDetailView):
    model = Article

class ArticleCreateView(LoginRequiredMixin, View):
    model = Article
    template_name = 'ads/article_form.html'
    success_url = reverse_lazy('ads:all')
    # List the fields to copy from the Article model to the Article form
    fields = ['title', 'price','text']
    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        article = form.save(commit=False)
        article.owner = self.request.user
        article.save()
        form.save_m2m()
        return redirect(self.success_url)

class ArticleUpdateView(LoginRequiredMixin, View):
    model = Article
    template_name = 'ads/article_form.html'
    success_url = reverse_lazy('ads:all')
    fields = ['title', 'price','text']

    # This would make more sense
    # fields_exclude = ['owner', 'created_at', 'updated_at']

    def get(self, request, pk):
        pic = get_object_or_404(Article, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Article, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)


class ArticleDeleteView(OwnerDeleteView):
    model = Article
    template_name = 'ads/article_confirm_delete.html'
    success_url = reverse_lazy('ads:all')
def stream_file(request, pk):
    pic = get_object_or_404(Article, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Article, id=pk)
        fav = Fav(user=request.user, article=t)
        try:
            print('fav')
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            print('error fav')
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Article, id=pk)
        try:
            print('unfav')
            fav = Fav.objects.get(user=request.user, article=t).delete()
        except Fav.DoesNotExist as e:
            print('error unfav')

        return HttpResponse()