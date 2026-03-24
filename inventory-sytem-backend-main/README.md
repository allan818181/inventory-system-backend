Inventory Backend — setup & API examples

Setup (Windows PowerShell)
1. python -m venv venv
2. .\venv\Scripts\Activate.ps1
3. pip install -r requirements.txt
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py runserver

Notes:
- Ensure SECRET_KEY and DEBUG set appropriately in inventory/settings.py for production.
- If running frontend on a different origin, install/configure django-cors-headers and add origins.

API examples (use http://127.0.0.1:8000)

1) Signup (creates user + returns tokens)
curl -X POST http://127.0.0.1:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"secret123"}'

Response contains "access" and "refresh".

2) Login (obtain tokens)
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test@example.com","password":"secret123"}'

3) Google OAuth placeholder
curl -X POST http://127.0.0.1:8000/api/auth/google/ \
  -H "Content-Type: application/json" \
  -d '{"token":"GOOGLE_ID_TOKEN"}'

4) List products (public GET)
curl http://127.0.0.1:8000/api/products/

5) Create product (authenticated)
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"name":"Widget","category":"Tools","quantity":10,"min_stock_level":3,"cost_price":"5.00","selling_price":"9.99","supplier_id":1,"image_url":""}'

6) Update product
curl -X PUT http://127.0.0.1:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"name":"Widget v2","quantity":15}'

7) Delete product
curl -X DELETE http://127.0.0.1:8000/api/products/1/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

8) Low-stock alerts (frontend)
curl http://127.0.0.1:8000/api/alerts/low-stock/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

9) Stock movements
- List:
  curl http://127.0.0.1:8000/api/stock-movements/
- Create:
  curl -X POST http://127.0.0.1:8000/api/stock-movements/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <ACCESS_TOKEN>" \
    -d '{"product_id":1,"change":-2,"reason":"sale","note":"Sold 2 units"}'

10) Suppliers
- List:
  curl http://127.0.0.1:8000/api/suppliers/
- Create:
  curl -X POST http://127.0.0.1:8000/api/suppliers/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <ACCESS_TOKEN>" \
    -d '{"name":"Acme Co","contact_email":"supplier@example.com","phone":"123456","address":"Street 1"}'

11) Reports
- Low stock:
  curl http://127.0.0.1:8000/api/reports/low-stock/ \
    -H "Authorization: Bearer <ACCESS_TOKEN>"
- Fast moving:
  curl http://127.0.0.1:8000/api/reports/fast-moving/ \
    -H "Authorization: Bearer <ACCESS_TOKEN>"
- Sales vs Restock:
  curl http://127.0.0.1:8000/api/reports/sales-vs-restock/ \
    -H "Authorization: Bearer <ACCESS_TOKEN>"

12) Dashboard stats
- API dashboard:
  curl http://127.0.0.1:8000/api/dashboard/stats/ \
    -H "Authorization: Bearer <ACCESS_TOKEN>"
- Project-level dashboard path:
  curl http://127.0.0.1:8000/dashboard/stats/

If you want, I will:
- add a requirements-dev.txt or pin all dependency versions,
- register models in admin.py (if not already done),
- add django-cors-headers configuration,
- or create Postman collection.
