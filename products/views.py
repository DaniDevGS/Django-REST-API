from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ProductForm
from .serializers import ItemSerializer
from .models import Producto
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from rest_framework import generics
# Create your views here.
# Create your views here.
def home(request):
    """Renderiza la página de inicio.

    Esta vista simplemente devuelve la plantilla 'home.html'.

    Args:
        request: El objeto HttpRequest entrante.

    Returns:
        Un objeto HttpResponse que renderiza 'home.html'.
    """
    return render(request, 'home.html')

def signup(request):
    """Gestiona el registro de nuevos usuarios.

    Si es una solicitud GET, muestra el formulario de registro.
    Si es una solicitud POST, intenta crear un nuevo usuario y, si tiene éxito,
    inicia la sesión del usuario y lo redirige a la lista de tareas.
    Maneja errores si las contraseñas no coinciden o si el nombre de usuario
    ya existe.

    Args:
        request: El objeto HttpRequest entrante.

    Returns:
        Un objeto HttpResponse que:
        - Renderiza 'signup.html' con el formulario (GET).
        - Redirige a 'products' (POST exitoso).
        - Renderiza 'signup.html' con el formulario y un mensaje de error (POST fallido).
    """
    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('products')
            
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "User alredy exists"
                })

        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "Password do not match"
                })
    

@login_required
def products(request):
    
    product = Producto.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'products.html', {'productos': product})

@login_required
def products_to_send(request):
    product = Producto.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'products.html', {'product': product})

@login_required
def create_product(request):
    if request.method == 'GET':
        return render(request, 'create_product.html', {
            'form': ProductForm
        })
    else:
        try:
            form = ProductForm(request.POST)
            new_product = form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            return redirect('products')
        
        except ValueError:
            return render(request, 'create_product.html', {
                'form': ProductForm,
                'error': 'Porfavor provide valida data'
            })

@login_required
def product_detail(request, products_id:int):
    if request.method == 'GET':
        product = get_object_or_404(Producto, pk=products_id, user=request.user)
        form = ProductForm(instance=product)
        return render(request, 'products_detail.html', {'product': product, 'form': form})
    else:
        try:
            product = get_object_or_404(Producto, pk=products_id, user=request.user)
            form = ProductForm(request.POST, instance=product)
            form.save()
            return redirect('products')
        except ValueError:
            return render(request, 'task_detail.html', {'product': product, 'form': form, 'error': "Error updating task"})

def sent_product(request, products_id:int):
    # Productos enviados
    product = get_object_or_404(Producto, pk=products_id, user=request.user)
    if request.method == 'POST':
        product.datecompleted = timezone.now()
        product.save()
        return redirect('products')


def delete_product(request, products_id:int):
    product = get_object_or_404(Producto, pk=products_id, user=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('products')


@login_required
def signout(request):
    """Cierra la sesión del usuario actual y redirige a la página de inicio.

    Args:
        request: El objeto HttpRequest entrante.

    Returns:
        Un objeto HttpResponse que redirige a 'home'.
    """
    logout(request)
    return redirect('home')


def signin(request):
    """Gestiona el inicio de sesión del usuario.

    Si es una solicitud GET, muestra el formulario de autenticación.
    Si es una solicitud POST, intenta autenticar al usuario. Si tiene éxito,
    inicia la sesión del usuario y lo redirige a la lista de tareas. Si falla,
    muestra un mensaje de error.

    Args:
        request: El objeto HttpRequest entrante.

    Returns:
        Un objeto HttpResponse que:
        - Renderiza 'signin.html' con el formulario (GET).
        - Redirige a 'products' (POST exitoso).
        - Renderiza 'signin.html' con el formulario y un mensaje de error (POST fallido).
    """

    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'User or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('products')
        
class ItemListView(generics.ListAPIView):
    # 1. queryset: Define qué ítems se van a obtener (todos en este caso)
    queryset = Producto.objects.all()

    # 2. serializer_class: Indica qué serializador usar para convertir los ítems a JSON
    serializer_class = ItemSerializer