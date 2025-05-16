from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

from .models import CartItem, Category, OrderItem, Order


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['email'], password=data['password'])
        if user is not None:
            return JsonResponse({'status': 'success', 'message': 'Giriş başarılı'})
        else:
            return JsonResponse({'status': 'fail', 'message': 'Geçersiz bilgiler'})


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'status': 'fail', 'message': 'Bu kullanıcı adı zaten alınmış'})

        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        user.save()

        return JsonResponse({'status': 'success', 'message': 'Kayıt başarılı'})


# Ürünleri Listele
from .models import Product


def product_list(request):
    # Yalnızca GET isteği için işlem yapıyoruz
    if request.method == 'GET':
        products = Product.objects.all()
        product_data = [
            {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'description': product.description,
                'image': product.image if product.image else ''
            }
            for product in products
        ]
        return JsonResponse({'products': product_data})
    else:
        return JsonResponse({'message': 'Yalnızca GET isteği kabul edilmektedir.'}, status=405)


def products_by_category(request, category_id):
    if request.method == 'GET':
        try:
            category = Category.objects.get(id=category_id)
            products = category.products.all()
            product_data = [
                {
                    'id': product.id,
                    'name': product.name,
                    'price': str(product.price),
                    'description': product.description,
                    'image': product.image,
                    'category': category.name
                }
                for product in products
            ]
            return JsonResponse({'products': product_data})
        except Category.DoesNotExist:
            return JsonResponse({'message': 'Kategori bulunamadı'}, status=404)
    else:
        return JsonResponse({'message': 'Sadece GET isteği yapılabilir.'}, status=405)


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
import json


@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            old_username = data.get('old_username')
            new_username = data.get('new_username')
            new_password = data.get('new_password')

            user = User.objects.get(username=old_username)

            changed = False  # Değişiklik kontrolü için bayrak

            # Kullanıcı adı değişikliği
            if new_username and new_username != old_username:
                if User.objects.filter(username=new_username).exists():
                    return JsonResponse({'status': 'fail', 'message': 'Yeni kullanıcı adı zaten kullanılıyor'})
                user.username = new_username
                changed = True

            # Şifre değişikliği
            if new_password:
                user.set_password(new_password)
                changed = True

            if changed:
                user.save()
                return JsonResponse({'status': 'success', 'message': 'Profil güncellendi'})
            else:
                return JsonResponse({'status': 'info', 'message': 'Herhangi bir değişiklik yapılmadı'})

        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Kullanıcı bulunamadı'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': f'Hata: {str(e)}'}, status=500)


@csrf_exempt
def get_user_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')

            user = User.objects.get(username=username)
            user_data = {
                'username': user.username,
                'email': user.email,
                'password': user.password,
            }

            return JsonResponse({'status': 'success', 'user': user_data})

        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Kullanıcı bulunamadı'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': f'Hata: {str(e)}'}, status=500)


@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            new_password = data.get('new_password')

            user = User.objects.get(username=username)
            user.password = make_password(new_password)
            user.save()

            return JsonResponse({'status': 'success', 'message': 'Şifre başarıyla güncellendi'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Kullanıcı bulunamadı'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)}, status=500)


# Sepete Ürün Ekle
@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            username = data.get('username')

            user = User.objects.get(username=username)
            product = Product.objects.get(id=product_id)

            cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()

            return JsonResponse({'message': 'Ürün sepete eklendi'})
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Ürün bulunamadı'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Kullanıcı bulunamadı'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Hata: {str(e)}'}, status=500)


@csrf_exempt
def view_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')

            user = User.objects.get(username=username)
            cart_items = CartItem.objects.filter(user=user)
            items = []
            for item in cart_items:
                items.append({
                    'product': item.product.name,
                    'image': item.product.image if item.product.image else '',  # Görsel URL'si
                    'quantity': item.quantity,
                    'total_price': item.product.price * item.quantity
                })
            return JsonResponse({'cart_items': items})
        except User.DoesNotExist:
            return JsonResponse({'message': 'Kullanıcı bulunamadı', 'cart_items': []}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Hata: {str(e)}', 'cart_items': []}, status=500)


@csrf_exempt
def update_cart_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            product_name = data.get('product_name')
            new_quantity = data.get('quantity')

            user = User.objects.get(username=username)
            product = Product.objects.get(name=product_name)
            cart_item = CartItem.objects.get(user=user, product=product)

            cart_item.quantity = new_quantity
            cart_item.save()

            return JsonResponse({'message': 'Sepet güncellendi'})
        except CartItem.DoesNotExist:
            return JsonResponse({'message': 'Ürün sepette bulunamadı'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Hata: {str(e)}'}, status=500)


@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            product_name = data.get('product_name')

            user = User.objects.get(username=username)
            product = Product.objects.get(name=product_name)
            cart_item = CartItem.objects.get(user=user, product=product)

            cart_item.delete()

            return JsonResponse({'message': 'Ürün sepetten silindi'})
        except CartItem.DoesNotExist:
            return JsonResponse({'message': 'Ürün sepette bulunamadı'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Hata: {str(e)}'}, status=500)


def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = [{'id': cat.id, 'name': cat.name} for cat in categories]
        return JsonResponse({'categories': data})


@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            address = data.get('address')

            user = User.objects.get(username=username)
            cart_items = CartItem.objects.filter(user=user)

            if not cart_items.exists():
                return JsonResponse({'status': 'fail', 'message': 'Sepet boş'})

            # Siparişi oluştur
            order = Order.objects.create(user=user, address=address)

            # Sepetteki ürünleri siparişe ekle
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

            # Sepeti temizle
            cart_items.delete()

            return JsonResponse({'status': 'success', 'message': 'Sipariş başarıyla oluşturuldu'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Kullanıcı bulunamadı'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': f'Hata: {str(e)}'}, status=500)


@csrf_exempt
def get_order_history(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')

            user = User.objects.get(username=username)
            orders = Order.objects.filter(user=user).order_by('-created_at')

            order_history = []

            for order in orders:
                items = OrderItem.objects.filter(order=order)
                item_list = [{
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'price': str(item.product.price),
                    'total_price': str(item.product.price * item.quantity),
                    'image': item.product.image if item.product.image else ''
                } for item in items]

                order_history.append({
                    'order_id': order.id,
                    'address': order.address,
                    'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'items': item_list
                })

            return JsonResponse({'status': 'success', 'orders': order_history})
        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Kullanıcı bulunamadı'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': f'Hata: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Sadece POST isteği yapılabilir'}, status=405)
