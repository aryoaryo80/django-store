from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from utils import IsAdminMixin
from .models import *
from .tasks import *
from .forms import *
from django.http import HttpResponse


class HomeView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if kwargs.get('category_slug'):
            category = get_object_or_404(
                Category, slug=kwargs['category_slug'])
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products': products, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['product_slug'])
        form = AddToCartForm
        return render(request, 'home/product_detail.html', {'product': product, 'form': form})


class BucketDetailView(IsAdminMixin, View):
    template_name = 'home/bucket_detail.html'

    def get(self, request, *args, **kwargs):
        objects = get_bucket_objects()
        return render(request, self.template_name, {'objects': objects})


class DeleteBucketObjectView(IsAdminMixin, View):
    def get(self, request, *args, **kwargs):
        delete_object.delay(kwargs['object_name'])
        messages.success(request, 'delete object has been started')
        return redirect('home:bucket_detail')


class DownloadBucketObjectView(IsAdminMixin, View):
    def get(self, request, *args, **kwargs):
        download_object.delay(kwargs['object_name'])
        messages.success(request, 'download object has been started')
        return redirect('home:bucket_detail')


class OkView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('successfully .loaded')
