from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import certifi
import sys
import json


class DBMongo():

    def __init__(self):

        USER = "Liverpool"
        PWD = "7MtvuaUWcD4Flr8X"
        CONNECTION_STRING = f"mongodb+srv://{USER}:{PWD}@appplantilla.fzlnsbp.mongodb.net/test"
        client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
        self.get_database = client['AppPlantillas']
        
   
    def queryString(self,query="",colleccion="Plantillas"):
        self.colleccion = colleccion
        self.collection_name = self.get_database[colleccion]
        data = {}
        rows = []
        cursor = self.collection_name.find(query)
        count=0
        for row in cursor:
            count+=1
            row["_id"] = str(row["_id"])
            rows.append(row)
            if count>=10:
                break

        data["resultado"] = rows
        return data
    
    def insertOneRow(self, data = {}):

        # newRow = {
        #     "first_name": "Gustavo",
        #     "last_name": "Mendoza",
        #     "company_name": "El Puerto de Liverpool",
        #     "address": "Coacalco",
        #     "city": "Mexico City",
        #     "county": "México",
        #     "state": "CDMX",
        #     "zip": 55705,
        #     "phone1": "55-34596395",
        #     "phone": "55-34596395",
        #     "email": "gusoda1992@gmail.com"
        #     }

        self.collection_name.insert_one(data)

    def insertManyRows(self):

        newRow1 = {
            "first_name": "Gustavo",
            "last_name": "Mendoza",
            "company_name": "El Puerto de Liverpool",
            "address": "Coacalco",
            "city": "Mexico City",
            "county": "México",
            "state": "CDMX",
            "zip": 55705,
            "phone1": "55-34596395",
            "phone": "55-34596395",
            "email": "gusoda1992@gmail.com"
            }
        newRow2 = {
            "first_name": "Ricardo",
            "last_name": "Mendoza",
            "company_name": "El Puerto de Liverpool",
            "address": "Coacalco",
            "city": "Mexico City",
            "county": "México",
            "state": "CDMX",
            "zip": 55705,
            "phone1": "55-34596395",
            "phone": "55-34596395",
            "email": "gusoda1992@gmail.com"
            }
    
        self.collection_name.insert_many([newRow1,newRow2])

    def DeleteRowByID(self, id = "6417a2dff37c32e864973116"):
    
        self.collection_name.delete_one({'_id': ObjectId(id)})

    def DeleteRowByQuery(self, query = {"email":"gusoda1992@gmail.com"}):
    
        self.collection_name.delete_many(query)

    def UpdateRowByID(self, id = "6417a66a9abe0b43ca1955b7", values = { "first_name": "Gustavo Ricardo" }):

        myQuery = {'_id': ObjectId(id) }
        newValues = { "$set": values }
        self.collection_name.update_one(myQuery, newValues)
    
    
#print(DBMongo().queryString(colleccion="Plantillas",query={"plantilla":"L3-1035562"}))
# try:
#     DBMongo().insertOneRow(data=
#     {"nombrePlantilla": "L4-737080",
#     "atributos":[
#         {   
#             "id":1,
#             "input1":"123211",
#             "input2":"234234"
#         },
#         {
#             "id":2,
#             "input1":"4234",
#             "input2":"435345"
#         },
#         {
#             "id":3,
#             "input1":"34534",
#             "input2":"2342342"
#         }
#     ],
#     "excepciones":[
#         {   
#             "id":1,
#             "input1":"123211",
#             "input2":"234234"
#         },
#         {
#             "id":2,
#             "input1":"123211",
#             "input2":"234234"
#         },
#         {
#             "id":3,
#             "input1":"123211",
#             "input2":"234234"
#         }
#     ]})
#     print("se inserto un registro")
# except:
#     print("error")
# DBMongo().insertManyRows()
# DBMongo().DeleteRowByID(id = "6417a66a9abe0b43ca1955b6")
# DBMongo().DeleteRowByQuery({"email":"gusoda1992@gmail.com"})
# DBMongo().UpdateRowByID(id = "6417a66a9abe0b43ca1955b7",values = { "first_name": "Maria Jose" })


