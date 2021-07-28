/* app2 = new Vue({
  el: '#app2',
  delimiters: ['[[', ']]'],
  data(){
    return {
      nombres:[],
      variable:[],
      valores:[]
    }
  },
  computed:{
    listado(){
      const path = 'http://upsilon.aasana.ga/pibrealtime'
      axios.get(path).then((respuesta) => {
        this.nombres = respuesta.data
        this.variable = [...new Set(this.nombres.map(lugar => lugar.lugar))]
        for(i=1;i<this.variable.length;i++){
          this.valores.push({lugar:this.variable[i]})
        }
      }).catch((error) => {
        console.log(error)
      })
    }
  }
}); */

app2 = new Vue({
  el: '#app2',
  delimiters: ['[[', ']]'],
  data(){
    return{
      nombres:[],
      datos:[],
      variable:[],
      valores:[],
      nombres2:[],
      par:[],
      impar:[],

      sw_parte1:false,
      sw_parte2:false,
      last_updated:""
    }
  },
  methods:{
    mensaje(){
      const path = 'http://upsilon.aasana.ga/pibrealtime'
      axios.get(path).then((respuesta) => {
        this.nombres2 = respuesta.data
      }).catch((error) => {
        console.log(error)
      })
    },

    listado(){
      const path = 'http://upsilon.aasana.ga/pibrealtime'
      axios.get(path).then((respuesta) => {

        this.par=[];
        this.impar=[];

        this.sw_parte1 = true;
        this.sw_parte2 = true;

        var fecha = String(respuesta.data[0].hora_actualizado).split(' ');
        this.last_updated = fecha[0] + "\n" + fecha[1].substr(0, 8) + ' UTC';


        this.nombres = respuesta.data
        this.variable = [...new Set(this.nombres.map(lugar => lugar.lugar))]
        /* console.log(this.variable) */

        for(i=1;i<this.variable.length;i++){
          if(i%2==0){
            this.par.push({lugar:this.variable[i],f:'f-'+i, h:'h-'+i, h2:'#h-'+i});
          }else{
            this.impar.push({lugar:this.variable[i],f:'f-'+i, h:'h-'+i, h2:'#h-'+i});
          }
        }
        //console.log(this.valores);
        /* for(i=0;i<this.nombres.length;i++){
          this.datos.push({f:'f-'+this.nombres[i].id, h:'h-'+this.nombres[i].id, h2:'#h-'+this.nombres[i].id});
        }
        console.log(this.datos); */
      }).catch((error) => {
        console.log(error)
      });

    },
    hola(){
      alert("hola mundo");
    }
    
    
  },
  
});