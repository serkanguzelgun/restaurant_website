from django.urls import path
from .views import login_user, register_user, place_order
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_user),
    path('register/', register_user),
    path('products/', views.product_list, name='product_list'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('products/category/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('categories/', views.category_list, name='category_list'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('get-user-profile/', views.get_user_profile, name='get_user_profile'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('place_order/', place_order),
    path('order-history/', views.get_order_history),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
