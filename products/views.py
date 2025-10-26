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
from rest_framework.permissions import IsAuthenticated
# Create your views here.
# Create your views here.
from rest_framework.decorators import api_view, permission_classes # New
from rest_framework.response import Response # New
from rest_framework import status # New
from rest_framework.permissions import AllowAny # New
from rest_framework.authtoken.models import Token # New - For Token Authentication
from django.views.decorators.csrf import csrf_exempt # New - For Signout


def home(request):
    """Renderiza la página de inicio.

    Esta vista simplemente devuelve la plantilla 'home.html'.

    Args:
        request: El objeto HttpRequest entrante.

    Returns:
        Un objeto HttpResponse que renderiza 'home.html'.
    """
    return render(request, 'home.html')

# API DE SIGNUP

@api_view(['POST'])
@permission_classes([AllowAny]) # Allow anyone to access this view
def signup_api(request):
    """API para registrar un nuevo usuario."""
    username = request.data.get('username')
    password = request.data.get('password')
    password2 = request.data.get('password2') # Assuming you send both passwords from the frontend

    if not all([username, password, password2]):
        return Response({'error': 'Todos los campos son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

    if password != password2:
        return Response({'error': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        
        # Crea un token para el nuevo usuario
        token, created = Token.objects.get_or_create(user=user)
        
        # Retorna el token al frontend
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_201_CREATED)
    
    except IntegrityError:
        return Response({'error': 'El nombre de usuario ya existe.'}, status=status.HTTP_400_BAD_REQUEST)
    

# API DE SIGNIN

@api_view(['POST'])
@permission_classes([AllowAny]) # Allow anyone to access this view
def signin_api(request):
    """API para iniciar sesión y obtener un token."""
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response({'error': 'Usuario o contraseña incorrectos.'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        # Obtiene o crea el token para el usuario
        token, created = Token.objects.get_or_create(user=user)
        
        # Retorna el token
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)

# API DE SIGNOUT
@api_view(['POST'])
def signout_api(request):
    """API para cerrar sesión (simplemente elimina el token de autenticación del usuario)."""
    # Esta vista requiere que el usuario envíe el token en el encabezado 'Authorization'
    if request.auth: # request.auth is the token object if authenticated
        try:
            # Elimina el token del usuario (invalida la sesión actual del API)
            request.auth.delete() 
            return Response({'message': 'Sesión cerrada exitosamente.'}, status=status.HTTP_200_OK)
        except Exception:
            # Si no se puede eliminar el token (por ejemplo, si ya se eliminó), al menos responde OK
            return Response({'message': 'Sesión cerrada exitosamente.'}, status=status.HTTP_200_OK)
    
    # En este caso, el token no estaba presente o era inválido, pero respondemos que la sesión está cerrada.
    return Response({'message': 'No hay sesión activa para cerrar.'}, status=status.HTTP_401_UNAUTHORIZED)


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
    
    productos = Producto.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'products.html', {'productos': productos})

@login_required
def products_to_send(request):
    productos = Producto.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'products.html', {'productos': productos})

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
        producto = get_object_or_404(Producto, pk=products_id, user=request.user)
        form = ProductForm(instance=producto)
        return render(request, 'products_detail.html', {'productos': producto, 'form': form})
    else:
        try:
            producto = get_object_or_404(Producto, pk=products_id, user=request.user)
            form = ProductForm(request.POST, instance=producto)
            form.save()
            return redirect('products')
        except ValueError:
            return render(request, 'products_detail.html', {'productos': producto, 'form': form, 'error': "Error updating product"})

def sent_product(request, products_id:int):
    # Productos enviados
    # Se asegura de obtener el producto SOLO si pertenece al usuario logueado
    producto = get_object_or_404(Producto, pk=products_id, user=request.user)
    if request.method == 'POST':
        # La condición se cumple: el producto existe y pertenece al usuario.
        # Se marca como 'enviado' (datecompleted)
        producto.datecompleted = timezone.now()
        producto.save()
        return redirect('products')


def delete_product(request, products_id:int):
    producto = get_object_or_404(Producto, pk=products_id, user=request.user)
    if request.method == 'POST':
        producto.delete()
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
    # Esto le dice a DRF que use ItemSerializer
    serializer_class = ItemSerializer 
    
    def get_queryset(self):
        # Esto obtiene TODOS los objetos Producto
        return Producto.objects.all().order_by('-created')