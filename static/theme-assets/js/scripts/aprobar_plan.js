/*
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

*/







//function agregar(){
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