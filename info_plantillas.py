import pandas as pd
import re
from database.mongodb import DBMongo

con = DBMongo()

df = pd.read_csv('data//plantillas_attr.csv')

filtro = [" ", "Data", "mirakl", "Mirakl","Reject","reject","Estatus","Evento","Fecha","Descuento","Costo",
                   "Date","Status","Mercancia","Impuesto","IVA"]

for row in filtro: 
    df.query(f'~att_id.str.contains("{row}")',inplace=True)

data = df.groupby(["plantilla"]).att_id.apply(list).reset_index()

json = data.to_json(orient ='records')

con.insertManyRows(data = json)