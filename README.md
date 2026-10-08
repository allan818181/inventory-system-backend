<h1 align="center">Inventory System: Backend API</h1>

<p align="center"><b>REST API for an inventory management system, secured with JWT. Frontend: [inventory-frontend](https://github.com/allan818181/inventory-frontend).</b></p>

<p align="center">![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white) ![Django REST](https://img.shields.io/badge/Django%20REST-A30000?logo=django&logoColor=white) ![JWT](https://img.shields.io/badge/JWT-000000?logo=jsonwebtokens&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)</p>

## Overview

Django REST Framework API for an inventory management system with JWT authentication (SimpleJWT) and a custom user model. Pairs with inventory-frontend.

## Features

- REST endpoints for products, suppliers and stock movements
- JWT access/refresh tokens (djangorestframework-simplejwt)
- Custom user model
- Serializers and URL routing kept in a single `api` app

## Tech stack

Python · Django · Django REST · JWT · SQLite

## Getting started

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver      # http://127.0.0.1:8000
```

## Project structure

`inventory/` settings · `api/` models, serializers, views, urls

---

<p align="center">Built by <a href="https://github.com/allan818181"><b>Allan Muganyizi Deus</b></a> · Full-Stack &amp; DevOps Engineer · Dar es Salaam, Tanzania<br/>
<a href="https://www.linkedin.com/in/allan-deus-4b888631a">LinkedIn</a> · <a href="mailto:allandeus014@gmail.com">Email</a></p>
