from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()

#struktur data sesuai di pdf
class Data(BaseModel):
    # id:int
    product_name:str
    product_code:str
    qty:int
    expired_date:date
    warehouse_loc:str

#data contoh
data = [
    Data(product_name='Cimol Original'  ,product_code="CO",qty=3,expired_date=date(2025,5,1),warehouse_loc="Bandung"),
    Data(product_name='Cimol Mozzarella',product_code="CM",qty=5,expired_date=date(2025,6,1),warehouse_loc="Bandung"),
    Data(product_name='Cimol Spicy'     ,product_code="CS",qty=8,expired_date=date(2025,7,1),warehouse_loc="Bandung"),
]

# data = [
#     Data(id=1,product_name='Cimol Original'  ,product_code="CO",qty=3,expired_date=date(2025,5,1),warehouse_loc="Bandung"),
#     Data(id=2,product_name='Cimol Mozzarella',product_code="CM",qty=5,expired_date=date(2025,6,1),warehouse_loc="Bandung"),
#     Data(id=3,product_name='Cimol Spicy'     ,product_code="CS",qty=8,expired_date=date(2025,7,1),warehouse_loc="Bandung"),
# ]

#produk semua + filtering
@app.get('/cimol',response_model=List[Data])
def cimol(
    product_name: Optional[str] = Query(None), 
    product_code: Optional[str] = Query(None),
    warehouse_doc: Optional[str] = Query(None),
    min_qty: Optional[int] = Query(None),
    max_qty: Optional[int] = Query(None),
):
        #jika tidak ada paramenter
        # if not product_name and not product_code and not min_qty and not max_qty : return data
        if not any([product_name, product_code, min_qty, max_qty, warehouse_doc]):
            return data
        
        #jika ada
        product_name = product_name.lower() if product_name else None
        product_code = product_code.lower() if product_code else None
        warehouse_doc  = warehouse_doc .lower() if warehouse_doc  else None

        result=[]
        for itm in data:
             match_name = product_name is None or product_name in itm.product_name.lower() 
             match_code = product_code is None or product_code in itm.product_code.lower()
             match_warehouse = warehouse_doc is None or warehouse_doc in itm.warehouse_loc.lower()

             match_min_qty = min_qty is None or min_qty <= itm.qty
             match_max_qty = max_qty is None or max_qty >= itm.qty

             match_text = match_name and match_code and match_warehouse
             match_qty = match_min_qty and match_max_qty

             if match_text and match_qty : result.append(itm)

        if not result:
            raise HTTPException(status_code=404, detail="Product Not Found!")
        
        return result
        
#produk specific
@app.get('/cimol/{product_code}',response_model=Data)
def cimol_product(product_code:str):
    for itm in data:
        if itm.product_code == product_code : return itm
    raise HTTPException(status_code=404, detail='Product not Found!')

#buat add
@app.post('/cimol/add')
def cimol_add(item:Data):
    #  use_id = max([d.id for d in data], default=0)
    #  item.id = use_id + 1
     for d in data:
          if d.product_code == item.product_code : 
               raise HTTPException(status_code=404,detail="Record with the same PRODUCT CODE already exists!")
     data.append(item)
     return {
                "msg": "Product successfully added!",
                "data": item
            }

#buat edit
@app.put('/cimol/edit')
def cimol_edit(item:Data):
    for idx, d in enumerate(data):
        if d.product_code == item.product_code: 
            data[idx]=item
            return {
                "msg": "Product successfully updated!",
                "data": item
            }
    raise HTTPException(status_code=404,detail="No record with that PRODUCT CODE exists!") 

@app.delete('/cimol/{product_code}/delete')
def cimol_edit(product_code:str):
    for idx, d in enumerate(data):
        if d.product_code == product_code: 
            data.pop(idx)
            return {
                "msg": "Product successfully deleted!"
            }
    raise HTTPException(status_code=404,detail="No record with that PRODUCT CODE exists!") 
