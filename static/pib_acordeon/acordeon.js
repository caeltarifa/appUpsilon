let pos=[13,26,39];
const exampleData1=[];
const exampleData2=[];
const exampleData3=[];

//DICCIONARIO DE DATOS
 const datos={

  'fecha_modificacion': '21-09-2021',
  'hora_modificacion': '15:25:45',
  'data' :
  [
    {'lugar':'SLCB' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLGY' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLLP' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLRQ' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLET' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLSU' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLTR' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLUY' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLVR' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLHI' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLRI' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLRY' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLPS' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLYA' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLAG' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLAP' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLAS' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' },{ 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLBJ' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLCA' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLCP' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLJE' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLJO' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLJV' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLMG' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLOR' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLPO' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLRA' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLRB' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLSA' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLSB' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLSI' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLSM' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLSR' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLTI' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLVG' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } , { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLVM' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLTJ' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] },
    {'lugar':'SLCX' , 'nombre_lugar': 'air_lugar' , 'nombre_aer':'nombre_pista', 'pib': [ { 'asunto':'asunto_x' , 'estado_asunto': 'esatado_y' , 'ref':'C0990/21' } ] }
]
}

function acordeon1()
{
  for (var j = 0; j < pos[0]; j++) 
  {
    //console.log(pos[j]);
    exampleData1[j]= {
      id: j,
      active: false,
      title: datos.data[j].lugar,
      details: 
      `Nombre_lugar : `+datos.data[j].nombre_lugar + `<br>`+
      `Nombre_aero : `+datos.data[j].nombre_aer + `<br><br>`+`
      <div class="tabla">           
      <table class="table table-striped">
      <thead>
        <tr>
          <th>Asunto</th>
          <th>Estado asunto</th>
          <th>Referencia</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>`+datos.data[j].pib[0].asunto+ `</td>
          <td>`+datos.data[j].pib[0].estado_asunto+ `</td>
          <td>`+datos.data[j].pib[0].ref+ `</td>
        </tr>
        <tr>
          <td>Mary</td>
          <td>Moe</td>
          <td>mary@example.com</td>
        </tr>
        <tr>
          <td>July</td>
          <td>Dooley</td>
          <td>july@example.com</td>
        </tr>
      </tbody>
     </table>
    </div>
    `
    }
  }
}

acordeon1();

/*
const exampleData2 = [
  {
    id: 1,
    active: false,
    title: 'Celebration',
    details: `
      <p>Come on, this is a Bluth family celebration. It's no place for children.</p>
    `
  },
  {
    id: 2,
    active: false,
    title: 'Lighter Fluid and Wine',
    details: `
      <p>But where did the lighter fluid come from? Wine only turns to alcohol if you let it sit. But anyhoo, can you believe that the only reason the club is going under is because it's in a terrifying neighborhood?</p>
    `
  },
  {
    id: 3,
    active: false,
    title: `What's in Oscar's box?`,
    details: `
      <p>In fact, it was a box of Oscar's legally obtained medical marijuana. Primo bud. Real sticky weed.</p>
      <p>Great, now I'm gonna smell to high heaven like a tuna melt!</p>
    `
  }
]

const exampleData3 = [
  {
    id: 1,
    active: false,
    title: 'Celebration',
    details: `
      <p>Come on, this is a Bluth family celebration. It's no place for children.</p>
    `
  }]*/

Vue.component('accordion', {
  props: {
    content: {
      type: Array,
      required: true
    },
    multiple: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      groupId: null
    }
  },
  template: `
    <dl class="accordion box" role="presentation">
      <accordion-item
        v-for="item in content"
        :multiple="multiple"
        :item="item"
        :groupId="groupId"
        :key="item.id">
      </accordion-item>
    </dl>
  `,
  mounted() {
    this.groupId = this.$el.id
  }
})

Vue.component('accordion-item', {
  props: ['item', 'multiple', 'groupId'],
  template: `
    <div :id="groupId + '-' + item.id" class="accordion-item" :class="{'is-active': item.active}">
      <dt class="accordion-item-title">
        <button @click="toggle" class="accordion-item-trigger">
          <h4 class="accordion-item-title-text">{{item.title}}</h4>
          <span class="accordion-item-trigger-icon"></span>
        </button>
      </dt>
      <transition
        name="accordion-item"
        @enter="startTransition"
        @after-enter="endTransition"
        @before-leave="startTransition"
        @after-leave="endTransition">
        <dd v-if="item.active" class="accordion-item-details">
          <div v-html="item.details" class="accordion-item-details-inner"></div>
        </dd>
      </transition>
    </div>
  `,
  methods: {
    toggle(event) {
      if (this.multiple) this.item.active = !this.item.active
      else {
        this.$parent.$children.forEach((item, index) => {
          if (item.$el.id === event.currentTarget.parentElement.parentElement.id) item.item.active = !item.item.active
          else item.item.active = false
        }) 
      }
    },
    
    startTransition(el) {
      el.style.height = el.scrollHeight + 'px'
    },
    
    endTransition(el) {
      el.style.height = ''
    }
  }
})

new Vue({
  el: '#app',
  data: {
    example1: exampleData1,
    example2: exampleData2,
    example3: exampleData3
  }
})