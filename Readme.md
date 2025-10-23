# Django-REST-API
Este proeycto es un sistema que tiene una API REST construida con el popular framework de **Django** (Python) para administrar los productos del repositortio de *ecommerce-nextjs-trv-smart-shop* de **luisguillermog**

## 🛠️ Stack Tecnológico

---
| Componente | Tecnología | Propósito |
| :--- | :---| :--- |
| **Backend** | [![Lenguajes and Frameworks](https://skillicons.dev/icons?i=py,django)](https://github.com/DaniDevGS/Demon-Slayer-API)| Servidor REST y logica de los productos. |
| **Base de Datos** | [![DataBase](https://skillicons.dev/icons?i=postgresql,sqlite)](https://github.com/DaniDevGS/Demon-Slayer-API) | Almacenamiento de los usuarios y los productos |
| **Frontend** | [![Layout](https://skillicons.dev/icons?i=html,bootstrap)](https://github.com/DaniDevGS/Demon-Slayer-API) | Maquetacion y estilos con bootstrap |
---

## 🚀 Instalación y Ejecución

Sigue estos pasos para levantar la app en tu entorno local.

### Prerequisitos

* **Python 3+**
* **`pip`** (Python package installer)

### 1. Clonar el Repositorio

```bash
git clone https://github.com/DaniDevGS/Django-REST-API.git
cd Django-REST-API
```

### 2. Crear Entorno Virtual e Instalar Dependencias

Se recomienda usar un entorno virtual para aislar las dependencias del proyecto.

```bash

# Crear entorno virtual (ej. venv)
python -m venv venv

# Activar el entorno virtual
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar depencias
pip install -r requirements.txt
```
### 3. Ejecutar la Aplicación

Ejecuta el servidor de Django:

```bash

python manage.py runserver
```

## 📚 Endpoints de la API

La API expone los siguientes puntos de conexión REST (actualmente solo soporta GET):

---
| Metodo | Endpoint | Descripción |
| :--- | :---| :--- |
| **GET** | **/api/products/?format=json** | Obtiene la lista completa de todos los productos enviados	 |
---

### Ejemplo: Obtener un Producto
Para obtener la información de Tanjiro Kamado (ID 1), haz una solicitud a:

```bash

GET [http://127.0.0.1:5000/api/characters/1](http://127.0.0.1:5000/api/characters/1)
```

### Respuesta (JSON):
```json
{
    "id": 1,
    "título": "iPhone 17",
    "description": "Celular de Apple",
    "precio": "1400.00",
    "fecha de finalización": nulo,
    "imagen": "http://localhost:8000/media/productos/iPhone17.jpg",
    "usuario": 1
  }
```


/api/products/?format=json