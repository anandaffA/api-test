# Simple API test

Simple api test using Python with FastAPI and Uvicorn.

installation guide:
1. install both "pip install fastapi uvicorn"
2. run this "uvicorn main:app --reload" , make sure environment folder is in the same place as main.py 

No database, only using an array of objects.

-- GET : /cimol
- View all available products with the following queries available:
- product_name (string)
- product_code (string)
- min_qty (int)
- max_qty (int)
- warehouse_loc (string)

-- GET : /cimol/{product_code}
- View a specific product using 'product_code' in the header url.

-- POST : /cimol/add
-- Request Body:{
    "product_name": "Cimol Seaweed",
    "product_code": "CSW",
    "qty": 5,
    "expired_date": "2025-06-01",
    "warehouse_loc": "Japan"
}
- Add a product, product_code cannot be the same and request will be rejected and return an error.
  
-- PUT : /cimol/edit
-- Request Body: same as add
- Edit a product, if the back-end couldn't find a product with the corresponding product_code, it will return an error.

-- DELETE /cimol/{product_code}/delete
- Delete a specific product using 'product_code' in the header url.

- Anandaffa Apriadi (2025)
