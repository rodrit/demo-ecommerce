# demo-ecommerce

## Requerimientos

Python 3.6

- Django==3.1.2
- djangorestframework==3.12.1
- djangorestframework-simplejwt==4.4.0


Endpoints disponibles

### Autenticación:
- /api-auth/login/
- /api/token/
- /api/token/refresh/

### Lists (GET):
- /orders/?format=json
- /products/?format=json

### Details (GET):
- /orders/<int:id>/?format=json
- /products/<int:id>/?format=json

### Creations (POST):
- /products/

example:
	 { "name":"vaso", "price":10 }
	 
- /orders/

example:
```javascript
	{
	"date_time":"2020-10-26T21:19:05",
	"details":[
				{
					"cuantity":2,
					"product":1
				},
				{
					"cuantity":10,
					"product":2
				}
			]
	}
```

### Updates (PUT/PATCH):
- /producs/<int:id>/
- /orders/<int:id>/
	
Mismo formato de datos que en la creación. (formato parcial para PATCH)

### Deletions (DELETE):
- /producs/<int:id>/
- /orders/<int:id>/

### Pruebas con API  test-clients (Postman/RESTer). Obtener CSRF y JWT:
1.Setear header X-CSRFToken luego de hacer GET sobre '/api-auth/login/'  
2.Setear header Authorization (JWT + {token}) luego de hacer POST con credenciales validas a '/api/token/'  
3.Realizar las request sobre los endpoints disponibles  

