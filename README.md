# FastAPI-Ecommerce-API

## Introduction

FastAPI-Ecommerce-API is a RESTful backend service designed for an e-commerce platform.  
It is built using **FastAPI**, **MongoDB Atlas**, and **Motor (async driver)**, following a clean and modular architecture.

The API supports CRUD operations for clients, admins, products, orders, and payment transactions, using asynchronous processing and dependency injection.

This README is available in both **English and Spanish**.


---

<details>
<summary><strong>FastAPI-Ecommerce-API | English</strong></summary>

## Description

FastAPI-Ecommerce-API provides a scalable and asynchronous backend for an e-commerce system.  
It uses MongoDB Atlas as a NoSQL database and follows best practices for clean architecture:

- Modular routes
- Service layer abstraction
- Pydantic schemas for validation
- Async MongoDB access with Motor
- Dependency injection for database access

---

## Project Structure

```sh
app/
├── models/            # Domain models
├── schemas/           # Pydantic schemas (request/response)
├── services/          # Business logic layer
├── routes/            # API routes (endpoints)
├── config.py          # Database configuration
├── main.py            # FastAPI application entry point
├── .env               # Environment variables
requirements.txt
README.md
.gitignore
```
## Installation and Usage
### 1. Clone the repository

```sh
git clone https://github.com/camilotenorio1234/FastAPI-Ecommerce-API.git
cd FastAPI-Ecommerce-API

```

### 2. Create virtual environment
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Environment variables

Create a .env file:


```env
MONGODB_URI=**************** PORT=8000
```
### 5. Run the API

```sh
uvicorn app.main:app --reload
```
API will be available at:

```sh
http://127.0.0.1:8000
```
## Available Endpoints

### Clients
- POST /clientes
- GET /clientes
- GET /clientes/{id}
- PUT /clientes/{id}
- DELETE /clientes/{id}

### Products
- POST /productos
- GET /productos
- GET /productos/{id}

### Orders
- POST /ordenes
- GET /ordenes
- POST /ordenes/{id}/procesar_pago


### Payments
- POST /pagos
- GET /pagos/{id}

### Technologies Used
- FastAPI
- MongoDB Atlas
- Motor (Async MongoDB Driver)
- Pydantic
- Uvicorn
- Python 3.12
</details>

<details>
<summary><strong>FastAPI-Ecommerce-API | Español</strong></summary>

## Descripción

FastAPI-Ecommerce-API es un backend RESTful diseñado para una plataforma de comercio electrónico.  
Utiliza **FastAPI**, **MongoDB Atlas** y una arquitectura asíncrona con **Motor**, siguiendo buenas prácticas de diseño, escalabilidad y desarrollo modular.

El sistema soporta operaciones CRUD para clientes, administradores, productos, órdenes y transacciones de pago, utilizando procesamiento asíncrono, inyección de dependencias y validación de datos con Pydantic.


---

## Estructura del Proyecto

```sh
app/
├── models/            # Modelos de dominio
├── schemas/           # Esquemas Pydantic (request/response)
├── services/          # Lógica de negocio
├── routes/            # Endpoints de la API
├── config.py          # Configuración de la base de datos
├── main.py            # Punto de entrada de FastAPI
├── .env               # Variables de entorno
requirements.txt
README.md
.gitignore
```

## Instalación y Uso
1. Clonar el repositorio

```sh
git clone https://github.com/camilotenorio1234/FastAPI-Ecommerce-API.git
cd FastAPI-Ecommerce-API
```

2. Crear entorno virtual

```sh
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias


```
pip install -r requirements.txt
```

4. Variables de entorno

Crear archivo .env dentro de app/:
```sh
MONGODB_URI=**************** PORT=8000
```

5. Ejecutar la API

```sh
uvicorn app.main:app --reload
```
La API quedará disponible en:

```sh
http://127.0.0.1:8000
```
## Endpoints disponibles

### Clientes
- POST /clientes
- GET /clientes
- GET /clientes/{id}
- PUT /clientes/{id}
- DELETE /clientes/{id}

### Productos
- POST /productos
- GET /productos
- GET /productos/{id}

### Órdenes
- POST /ordenes
- GET /ordenes
- POST /ordenes/{id}/procesar_pago

### Pagos
- POST /pagos
- GET /pagos/{id}

## Tecnologías
- FastAPI
- MongoDB Atlas
- Motor (Async MongoDB Driver)
- Pydantic
- Uvicorn
- Python 3.12

</details>
