from flask import Flask, render_template, request
from database.mongodb import DBMongo
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

conexion = DBMongo()



def query():
    dropdown1= conexion.queryString(colleccion="Plantillas")
    plantillas = [i["plantilla"] for i in dropdown1["resultado"]]
    jsonRaw = {}
    for i in dropdown1["resultado"]:
        jsonRaw[i['plantilla']]=i['att_id']
        
    #print(jsonRaw)
    #print(plantillas)
    if request.method == 'POST':
        
    
        jsonResponse = app.response_class(
                    response=json.dumps(jsonRaw),
                    status=200,
                    mimetype='application/json'
                                            )
        return jsonResponse


@app.route('/', methods=['GET', 'POST'])
def formulario():
    print(request.form)
    dropdown1= conexion.queryString(colleccion="Plantillas")
    
    
    
    filas = []
    excepcionesor = ""
    excepciones = ""
    strexcep = ""
    strexcep_and = []
    plantilla = str("Niunguna plantilla Seleccionada")
    res_json = ""
    drpatt = ""
    excepcion1 = ""
    excepcion2 = ""
    excepcion3 = ""
    inputs1 = ""
    inputs2 = ""
    resultado = []
    try:
        if request.method == 'POST':
            print("datos recibidos",request.form)
            plantilla = str(request.form['plantilla']).upper()
            excepcionesor = request.form.getlist("or")
            strexcep_and = request.form.getlist("cond_and")
            
            #print(conexion.queryString(colleccion="Plantillas",query={"plantilla":"L3-1035562"}))
            drpatt = conexion.queryString(colleccion="Plantillas",query={'plantilla':str(plantilla)})
            #print(plantilla)
            drpatt =(drpatt['resultado'][0]["att_id"])
            #plantilla = request.form.getlist("plantilla")
            inputs1 = list(request.form.getlist('input1[]'))
            inputs2 = list(request.form.getlist('input2[]'))
            try:
                #print(len(inputs1))
                if len(inputs1)>0:
                    inputs1 = "+".join(inputs1)
                    inputs2 = "+".join(inputs2)
            
                excepcion1 = request.form.getlist('inputExcepcion1[]')
                excepcion2 = request.form.getlist('inputExcepcion2[]')
                excepcion3 = request.form.getlist('inputExcepcion3[]')
                if len(excepcion1)>0:
                    excepcion1 = "+".join(excepcion1)
            except:
                pass
            strexcep = []
            exce_and = ""
            acc_and = ""

            # if len(excepcionesor)>1 or len(strexcep_and)>1:
            #     resultado.append("SI")
            #     print(resultado)
            strexcep = []
            try:
                print(len(excepcionesor))
                if len(excepcionesor)>1:
                    strexcep.append("SI")
                    for i in range(len(excepcionesor)):
                        excepciones = f'(<{excepcionesor[i]}>  {request.form.getlist("cond_or")[i]} "{request.form.getlist("inp_or")[i]}")'
                        strexcep.append(excepciones)
                        strexcep.append("OR")
                    attomit = [f'<{x}>' for x in request.form.getlist("Omitir")]
                    attomit = " ".join(attomit)
                    palabra = f'entonces omitir {attomit} renombrar "{request.form.getlist("renombrar")[0]}"'
                    strexcep.append(palabra)
                elif len(excepcionesor)==0:
                    strexcep.append(" ")
                else:
        
                    strexcep.append("SI")
                    excepciones = f'(<{excepcionesor[0]}>  {request.form.getlist("cond_or")[0]} "{request.form.getlist("inp_or")[0]}")'
                    strexcep.append(excepciones)
                


                strexcep = " ".join(strexcep)
                print(strexcep) 
                #excepciones and
                if len(excepcionesor)>1:
                    strexcep.append("SI")
                    for i in range(len(excepcionesor)):
                        excepciones = f'((<{request.form.getlist("atributos")[i]}>  {request.form.getlist("cond_and")[i]} "{request.form.getlist("inp_and")[i]}" )Y ({request.form.getlist("and2")[i]} {request.form.getlist("cond_and1")[i]} {request.form.getlist("inputExcepcion3[]")[i]})'
                        strexcep.append(excepciones)
                        strexcep.append("OR")
                    attomit = [f'<{x}>' for x in request.form.getlist("Omitir")]
                    attomit = " ".join(attomit)
                    palabra = f'entonces omitir {attomit} renombrar "{request.form.getlist("renombrar")[0]}"'
                    strexcep.append(palabra)
                else:
                    strexcep.append("SI")
                    excepciones = f'(<{excepcionesor[0]}>  {request.form.getlist("cond_or")[0]} "{request.form.getlist("inp_or")[0]}")'
                    strexcep.append(excepciones)
           
            

                strexcep = " ".join(strexcep)
                print(strexcep)

            except:
                print("algun error") 
                

            res =({
        "nombrePlantilla": plantilla,
        "atplantilla":filas,
        "excepciones":excepciones})
            res_json = json.dumps(str(request.form))
 
        return render_template('formulario.html',excepcioneshtml=strexcep,at1=inputs1,at2=inputs2,atributos=drpatt,res=res_json,filas=filas, excepciones=excepciones,plantilla=plantilla,data=dropdown1)
    except:
        return render_template('formulario.html', at1=inputs1,at2=inputs2,atributos=drpatt,res=res_json,filas=filas, excepciones=excepciones,plantilla=plantilla,data=dropdown1)
@app.route("/Crear")
def crear():
    return '<h1>Formularo Para la creacion de una Plantilla</h1>'

@app.route('/plantillas',methods=['GET', 'POST'])
def consulta():
    print(request.form)
    return query()


if __name__ == '__main__':
    app.run(debug=True)