from django.urls import path, include
from . import views


app_name = 'home'

bucket_patterns = [
    path('bucket_detail/', views.BucketDetailView.as_view(), name='bucket_detail'),
    path('delete-bucket-object/<path:object_name>', views.DeleteBucketObjectView.as_view(),
         name='delete_bucket_object'),
    path('download-bucket-object/<path:object_name>',
         views.DownloadBucketObjectView.as_view(), name='download_bucket_object'),
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('ok/', views.OkView.as_view(), name='ok'),
    path('category/<slug:category_slug>/',
         views.HomeView.as_view(), name='category_detail'),
    path('product/<slug:product_slug>/',
         views.ProductDetailView.as_view(), name='product_detail'),

    path('bucket/', include(bucket_patterns)),

]
