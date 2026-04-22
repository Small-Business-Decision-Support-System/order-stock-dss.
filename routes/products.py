# routes/products.py — contains all API endpoints related to products

from fastapi import APIRouter  
# APIRouter lets us group related endpoints together in one file

from database import get_connection  
# we import our database connection function

router = APIRouter()  
# we create a router instance — this will be imported in main.py

@router.get("/products")  
# GET /products — returns all products from the database
def get_products():
    conn = get_connection()  
    # open a connection to PostgreSQL
    
    cursor = conn.cursor()  
    # cursor is the tool we use to run SQL queries
    
    cursor.execute("SELECT * FROM products")  
    # SQL query that fetches every row from the products table
    
    rows = cursor.fetchall()  
    # fetchall() collects all the returned rows into a Python list
    
    cursor.close()  
    # close the cursor after we're done using it
    
    conn.close()  
    # close the database connection to free up memory
    
    return {"products": rows}  
    # return the list of products as a JSON response

@router.post("/inventory/update")  
# POST /inventory/update — updates the stock level of a product
def update_inventory(product_id: int, quantity: int):
    # product_id — which product we're updating
    # quantity — how many units were sold or added
    
    conn = get_connection()  
    # open database connection
    
    cursor = conn.cursor()  
    # create cursor
    
    cursor.execute(
        "UPDATE products SET current_stock = current_stock - %s WHERE id = %s",
        (quantity, product_id)
    )  
    # SQL query that reduces the current_stock by the sold quantity
    # %s are placeholders — psycopg2 fills them safely to prevent SQL injection
    
    conn.commit()  
    # commit() saves the changes permanently to the database
    # without this line the changes would be lost
    
    cursor.close()
    conn.close()
    
    return {"message": "Stock updated successfully"}  
    # confirm to the frontend that the update worked