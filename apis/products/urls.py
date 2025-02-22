from django.urls import path

from apis.products.views import ProductViewSet

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'products', ProductViewSet, basename='products')
urlpatterns = router.urls
#
# urlpatterns = [
#     path('products/', ProductList.as_view()),
#     path('products/create/', ProductCreate.as_view()),
#     path('products/<uuid:pk>/detail/', ProductDetail.as_view()),
#     path('products/<uuid:pk>/delete/', ProductDelete.as_view()),
# ]
