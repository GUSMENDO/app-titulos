// Configuramos las opciones de la solicitud POST.
//let plantillaSeleccionada = ""
const options = {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    key: 'value'
    // Aquí puedes incluir cualquier dato que necesites enviar con la solicitud POST.
  })
};
let atributos_arr = []
// Hacemos una solicitud POST a la dirección 

const url ="http://127.0.0.1:5000/plantillas"
fetch(url, options)
.then(response => response.json())
.then(data => {
  const plantillas = data; // Accedemos al array de plantillas
  console.log(plantillas)
  const select = document.getElementById("plantillas");

  Object.keys(plantillas).forEach((key) => {
    const plantilla = key;
    const option = document.createElement("option");
    option.value = plantilla;
    option.text = plantilla;
    select.appendChild(option);
  });    
})
.catch(error => console.error(error));

function atributos(id) {


window.addEventListener("DOMContentLoaded", () => {
  
  const plantillasDropdown = document.getElementById("plantillas");
  //console.log(plantillasDropdown.value)

  plantillasDropdown.addEventListener("change", () => {
  atributos_arr = []
  let plantillaSeleccionada = plantillasDropdown.value;
  document.getElementById("add_row").disabled = false;
  document.getElementById("inpatt").disabled = false;
  document.getElementById("atributos").disabled = false;
  console.log("habilitando el boton")
  const url ="http://127.0.0.1:5000/plantillas"
fetch(url, options)
.then(response => response.json())
.then(data => {
  const plantillas = data; // Accedemos al array de plantillas
  //console.log(plantillas)
  const select1 = document.getElementById(id);
  select1.innerHTML = "";
  select1.innerHTML = "<option value=''>Palabra fija</option>";    
  (plantillas[plantillaSeleccionada]).forEach((i) => {
    //console.log(i)
    const option1 = document.createElement("option");
    option1.value = i;
    option1.text = i;
    select1.appendChild(option1);
    atributos_arr.push(i);
    
  }); 
  
  
})
.catch(error => console.error(error));  
  console.log(plantillaSeleccionada)
  })
  
      // Tu código aquí
});
}

atributos("atributos")


let id_atributos = 0
function agregarFila() {

console.log("se ejecuto")       
var tabla = document.getElementById("tabla-filas");
var fila = tabla.insertRow(-1);
var celda1 = fila.insertCell(0);
var celda2 = fila.insertCell(1);
var celda3 = fila.insertCell(2);
celda1.innerHTML = '<input type="text" class="form-control" name="input1[]">';
celda2.innerHTML = '<td></td>';
celda2.innerHTML = '<select id="atributos" class="form-control" name="input2[]"><option value="Palabrafija">Palabrafija</option></select>'
for (let i in atributos_arr) {
  celda2.querySelector("select").innerHTML += `<option value="${atributos_arr[i]}">${atributos_arr[i]}</option>`;
}


console.log('<select id="atributos1"><option value="Palabrafija">Palabrafija</option></select>')
celda3.innerHTML = '<button type="button" class="btn btn-danger" onclick="eliminarFila(this)">Borrar</button>';


}
let contador = 0;
function agregarExcepcion() {

var tabla = document.getElementById("tabla-excepciones");
var fila = tabla.insertRow(-1);
var celda1 = fila.insertCell(0);
var celda2 = fila.insertCell(1);
var celda3 = fila.insertCell(2);
var celda4 = fila.insertCell(3);
var celda5 = fila.insertCell(4);
var celda6 = fila.insertCell(5);
var celda7 = fila.insertCell(6);
celda4.innerHTML = '<td><select name="cond_or" id="inputExcepcion1[]"><option value="es igual a">es igual a</option><option value="es distinto a">es distinto a</option><option value="contiene la(s)">contiene la(s) palabra(s)</option><option value="no contiene la(s) palabra(s)">no contiene la(s) palabra(s)</option><option value="es nulo">es nulo</option><option value="no es nulo">no es nulo</option><option value="esta en">esta en</option><option value="no esta en">no esta en</option></select></td>';
celda5.innerHTML = '<input type="text" name="inp_or">';
celda3.innerHTML = '<td></td>';
celda3.innerHTML = '<select id="atributos" name="or"><option value="Palabrafija">Palabrafija</option></select>'
for (let i in atributos_arr) {
  celda3.querySelector("select").innerHTML += `<option value="${atributos_arr[i]}">${atributos_arr[i]}</option>`;
}

celda7.innerHTML = '<button type="button" class="btn btn-danger" onclick="eliminarFila(this)">Borrar</button>';
celda6.innerHTML = '<input type="button" value="O" onclick="agregarExcepcion()"><br><br>'
// Agregar tabla solo la primera vez que se llama a la función
if (contador == 0) {
  // Crear tabla
  var tablaNueva = document.createElement("table");
  tablaNueva.setAttribute("id", "tabla-nueva");
  // Crear filas
  var fila1 = tablaNueva.insertRow(0);
  var fila2 = tablaNueva.insertRow(1);
  var fila3 = tablaNueva.insertRow(2)
  // Crear celdas y añadir contenido

  var celda1Fila1 = fila1.insertCell(0);
  celda1Fila1.innerHTML = "<br><br><br><p>Entonces</p>";
  
  var celda1Fila2 = fila2.insertCell(0);
  celda1Fila2.innerHTML = "Omitir los campos	";
  var celda2Fila2 = fila2.insertCell(1);
  
  celda2Fila2.innerHTML = '<select id="Omitir" name="Omitir"><option value="Palabrafija">Palabrafija</option></select>';
  for (let i in atributos_arr) {
  celda2Fila2.querySelector("select").innerHTML += `<option value="${atributos_arr[i]}">${atributos_arr[i]}</option>`;
  }
  var celda1Fila3 =fila3.insertCell(0);
  celda1Fila3.innerHTML = '<td><label for="renombrar">Renombrar los campos                    Cambiar</label></td>';

  var celda2Fila3 =fila3.insertCell(1);
  
  celda2Fila3.innerHTML = '<select id="Omitir" name="renombrar"><option value="Palabrafija">Palabrafija</option></select>';
  for (let i in atributos_arr) {
  celda2Fila3.querySelector("select").innerHTML += `<option value="${atributos_arr[i]}">${atributos_arr[i]}</option>`;
  }

  var celda3Fila3 =fila3.insertCell(2);
  celda3Fila3.innerHTML = '<td><label for="por">Por</label></td>';
  
  celda3Fila3.innerHTML = "<p>Por</p>";
  var celda4Fila3 = fila3.insertCell(3);
  var celda4Fila3 = fila3.insertCell(3);
  celda4Fila3.innerHTML = '<input list="miDataList"><datalist id="miDataList" name="cambiarpor"></datalist>';
  //var datalist = celda4Fila3.querySelector("datalist");
  const datalist = document.getElementById('miDataList');
  //const array = ['valor3', 'valor4', 'valor5'];
  const option = document.createElement('option');
  
  // for (let i = 0; i < atributos_arr.length; i++) {
  //   const option = document.createElement('option');
  //   option.value = atributos_arr[i];
  //   option.textContent = atributos_arr[i];
  //   datalist.appendChild(option);
  // }

  // Insertar tabla debajo de la tabla de excepciones
  tabla.parentNode.insertBefore(tablaNueva, tabla.nextSibling);
contador ++;
}


}

function entonces() {

  // Crear tabla
  var tablaNueva = document.createElement("table");
  tablaNueva.setAttribute("id", "tabla-nueva");
  // Crear filas
  var fila1 = tablaNueva.insertRow(0);
  var fila2 = tablaNueva.insertRow(1);
  var fila3 = tablaNueva.insertRow(2)
  // Crear celdas y añadir contenido

  var celda1Fila1 = fila1.insertCell(0);
  celda1Fila1.innerHTML = "<br><br><br><p>Entonces</p>";
  
  var celda1Fila2 = fila2.insertCell(0);
  celda1Fila2.innerHTML = "Omitir los campos	";
  var celda2Fila2 = fila2.insertCell(1);
  
  celda2Fila2.innerHTML = '<select id="Omitir" name="Omitir"><option value="Palabrafija">Palabrafija</option></select>';
  for (let i in atributos_arr) {
  celda2Fila2.querySelector("select").innerHTML += `<option value="${atributos_arr[i]}">${atributos_arr[i]}</option>`;
  }
  var celda1Fila3 =fila3.insertCell(0);
  celda1Fila3.innerHTML = '<td><label for="renombrar">Renombrar los campos                    Cambiar</label></td>';

  var celda2Fila3 =fila3.insertCell(1);
  
  celda2Fila3.innerHTML = '<select id="Omitir" name="renombrar"><option value="Palabrafija">Palabrafija</option></select>';
  for (let i in atributos_arr) {
  celda2Fila3.querySelector("select").innerHTML += `<option value="${atributos_arr[i]}">${atributos_arr[i]}</option>`;
  }

  var celda3Fila3 =fila3.insertCell(2);
  
  celda3Fila3.innerHTML = '<td><label for="por">Por</label></td>';
  //celda3Fila4.innerHTML = 'button'
  celda3Fila3.innerHTML = "<p>Por</p>";
  var celda4Fila3 = fila3.insertCell(3);
  celda4Fila3.innerHTML = '<input list="miDataList"><datalist id="Omitir" name="cambiarpor"></datalist>';
  //var datalist = celda4Fila3.querySelector("datalist");
  // for (let i in atributos_arr) {
  //   var option = document.createElement("option");
  //   option.value = atributos_arr[i];
  //   option.textContent = atributos_arr[i]
  //   datalist.appendChild(option);
  // }

  // Insertar tabla debajo de la tabla de excepciones
  tabla.parentNode.insertBefore(tablaNueva, tabla.nextSibling);


}




let numFila = 1;

function and() {
let tabla = document.getElementById("tabla-excepciones");
let nuevaFila = tabla.insertRow(-1);

let celda1 = nuevaFila.insertCell(0);


let celda2 = nuevaFila.insertCell(1);
celda1.innerHTML = '<td><select name="atributos" id="atributos' + numFila + '"><option value="Palabrafija">Palabrafija</option></select></td>';
//let atributos_arr = ["Palabrafija", "Email", "Nombre", "Apellido", "Edad", "Direccion"]
celda2.innerHTML = '<td><select name="cond_and" id="inputExcepcion1' + numFila + '"><option value="es igual a">es igual a</option><option value="es distinto a">es distinto a</option><option value="contiene la(s)">contiene la(s) palabra(s)</option><option value="no contiene la(s) palabra(s)">no contiene la(s) palabra(s)</option><option value="es nulo">es nulo</option><option value="no es nulo">no es nulo</option><option value="esta en">esta en</option><option value="no esta en">no esta en</option></select></td>';
for (let i in atributos_arr) {
  celda1.querySelector("select").innerHTML += `<option value="${atributos_arr[i]}">${atributos_arr[i]}</option>`;
}

let celda3 = nuevaFila.insertCell(2);
celda3.innerHTML = '<input type="text" name="inp_and">';

let celda4 = nuevaFila.insertCell(3);
celda4.innerHTML = '<input type="button" value="O" onclick="agregarExcepcion()">';

let celda5 = nuevaFila.insertCell(4);
celda5.innerHTML = '<br><tr><input type="button" class="btn btn-warning" value="Y" onclick="and()"></tr>';

let celda6 = nuevaFila.insertCell(5);

let celda7 =nuevaFila.insertCell(6);

let celda8 = nuevaFila.insertCell(7);
celda8.innerHTML = '<input type="text" name="inputExcepcion3[]">';
celda6.innerHTML = '<td></td>';
celda6.innerHTML = '<select id="atributos" name="and2"><option value="Palabrafija">Palabrafija</option></select>';
celda7.innerHTML = '<td><select name="cond_and1" id="inputExcepcion2' + numFila + '"><option value="es igual a">es igual a</option><option value="es distinto a">es distinto a</option><option value="contiene la(s)">contiene la(s) palabra(s)</option><option value="no contiene la(s) palabra(s)">no contiene la(s) palabra(s)</option><option value="es nulo">es nulo</option><option value="no es nulo">no es nulo</option><option value="esta en">esta en</option><option value="no esta en">no esta en</option></select></td>';
for (let i in atributos_arr) {
  celda6.querySelector("select").innerHTML += `<option value="${atributos_arr[i]}">${atributos_arr[i]}</option>`;
}
let celda9 = nuevaFila.insertCell(8);
celda9.innerHTML = '<button type="button" class="btn btn-danger" onclick="eliminarFila(this)">Borrar</button><br>';
celda11.innerHTML = '<input type="button" class="btn btn-info" value="O" onclick="agregarExcepcion()">';
celda12.innerHTML ='<br><tr><input type="button" value="Y" onclick="and()"></tr>';
}