$(document).ready(function () {
  var lbltext = document.getElementById('plan_vuelo').innerHTML;
  array = lbltext.split("-");
  var element = "";
  for (let i = 0; i < array.length; i++) {
      if (i == 0) {
          continue;
      } else {
          element = element + "-" + array[i] + "<br> ";
      }
  }
  document.getElementById('plan_vuelo').innerHTML = element;


});



function imprim2() {
  var mywindow = window.open('', 'PRINT');
  mywindow.document.write('<!DOCTYPE html><html><head>');
  mywindow.document.write('<style>		@page{   margin: 0;    		}		 body { margin: 3mm 17mm 5mm 0mm; }     .incline-line{      width: 100%;      margin: none;      margin-top: 0%;      margin-bottom: 0%;      transform: rotate(156deg);      border-color: black;    } .incline-line2{      width: 100%;      margin: none;      margin-top: 0%;      margin-bottom: 0%;      transform: rotate(164deg);      border-color: black;    } button { display:none; }</style>');
  mywindow.document.write('</head><body >');
  mywindow.document.write(document.getElementById('muestra').innerHTML);
  mywindow.document.write('</body></html>');
  mywindow.document.close(); // necesario para IE >= 10
  mywindow.focus(); // necesario para IE >= 10
  mywindow.print();
  mywindow.close();
  return true;
};


function eliminarStrip(id) {
  imagen = document.getElementById(id);
  if (!imagen) {
      alert("El elemento selecionado no existe");
  } else {
      padre = imagen.parentNode;
      padre.removeChild(imagen);
  }

};


function agregar(){
  //document.getElementById('lista_ruta').innerHTML+='<div class="row" id="lista_ruta">    <div id="output"></div>    <select data-placeholder="Choose tags ..." name="tags[]"  class="chosen-select">                {% for punto in todopuntos  %}            <option value="{{punto.puntoInicial}}">{{punto.puntoInicial}}</option>        {% endfor %}    </select>        <select name="" id="">        {% for ruta_x in todaruta %}            <option value="">{{ruta_x.nombre_ruta}}</option>        {% endfor %}    </select>     <div id="output2"></div>    <select data-placeholder="Choose tags ..." name="tags[]"  class="chosen-select2">        {% for punto in todopuntos  %}            <option value="{{punto.puntoInicial}}">{{punto.puntoInicial}}</option>        {% endfor %}    </select>          <button class=" btn btn-outline-danger" enabled>        <i class="ficon ft-minus"></i>    </button></div>';
  //var dato="{{ todopuntos.puntoInicial }}"
  //alert(dato);
  // var newdiv = document.createElement("div", {id: "creado"});
  // var newcontent = document.createTextNode("ELEMENTO CREADO"+ ' <select data-placeholder="Choose tags ..." name="tags[]"  class="chosen-select"> {% for punto in todopuntos  %} <option value="{{punto.puntoInicial}}">{{punto.puntoInicial}}</option>{% endfor %}</select>');  
  // newdiv.appendChild(newcontent);

  // document.getElementById('lista_ruta').appendChild(newdiv);

//   <div class="row" id="lista_ruta">
//     <div id="output"></div>
//     <select data-placeholder="Choose tags ..." name="tags[]"  class="chosen-select">        
//         {% for punto in todopuntos  %}
//             <option value="{{punto.puntoInicial}}">{{punto.puntoInicial}}</option>
//         {% endfor %}
//     </select>    

//     <select name="" id="">
//         {% for ruta_x in todaruta %}
//             <option value="">{{ruta_x.nombre_ruta}}</option>
//         {% endfor %}
//     </select> 

//     <div id="output2"></div>
//     <select data-placeholder="Choose tags ..." name="tags[]"  class="chosen-select2">
//         {% for punto in todopuntos  %}
//             <option value="{{punto.puntoInicial}}">{{punto.puntoInicial}}</option>
//         {% endfor %}
//     </select>  
    

//     <button class=" btn btn-outline-danger" enabled>
//         <i class="ficon ft-minus"></i>
//     </button>

// </div>
}




// function invertirRuta(){
//   var vector=document.getElementByClassName('strip');
//   document.getElementById('muestra').innerHTML="";
//   for( var i = vector.length-1 ; i >= 0; i++){
//     document.getElementById('muestra').innerHTML=vector[i];
//   }
// }

// function mostrarmensaje(){
//   alert('ACTIVADO!')
// } 