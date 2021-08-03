var map;

//ESTOS DATOS SERAN ENVIADOS DESDE EL SERVIDOR CON UNA PETICION GET CON VUEJS

//[
//  {'lugar':'la paz','latitude':21.213,'longitude':43.234},
//  {'lugar':'cochabamba','latitude':21.213,'longitude':43.234},
//  {'lugar':'santa cruz','latitude':21.213,'longitude':43.234}
//  .
//  .
//  .
//  .
//  {'lugar':'potosi','latitude':21.213,'longitude':43.234}
//]


// Init Open Street Maps
function initmap() {
    // set up the map
    map = new L.Map('map');
    var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom: 7, maxZoom: 8, attribution: osmAttrib});
    map.setView(new L.LatLng(-16.5, -65.15),5.5);
    map.addLayer(osm);
  
    //DICCIONARIO
    const dic=[
    {'nombre':'SLLF', 'longitude':	'-68.1822' , 'latitude':	'-16.7933'},
    
    {'nombre':'SLLP', 'longitude':	'-68.1922' , 'latitude':	'-16.5133'},
    {'nombre':'SLRQ', 'longitude':	'-67.498001' , 'latitude':	'-14.4275'},
    {'nombre':'SLSB', 'longitude':	'-66.7386111111' , 'latitude':	'-14.8577778'},
    {'nombre':'SLAP', 'longitude':	'-68.4119444444' , 'latitude':	'-14.7355556'},
    {'nombre':'SLCC', 'longitude':	'-69.0955963' , 'latitude':	'-16.1910992'},//*
    {'nombre':'SLOR', 'longitude':	'-67.075' , 'latitude':	'-17.9555556'},
    {'nombre':'SLRY', 'longitude':	'-65.149612' , 'latitude':	'-13.3333333333'},
    {'nombre':'SLUY', 'longitude':	'-66.830002' , 'latitude':	'-20.459999'},
    
    
    {'nombre':'SLCB', 'longitude':	'-66.177101' , 'latitude':	'-17.421'},
    {'nombre':'SLAL', 'longitude':	'-65.149612' , 'latitude':	'-19.246836'},
    {'nombre':'SLBJ', 'longitude':	'-64.3127777777' , 'latitude':	'-22.7733333'},
    {'nombre':'SLHI', 'longitude':	'-65.141502' , 'latitude':	'-16.98975'},
    {'nombre':'SLAG', 'longitude':	'-63.9627777777' , 'latitude':	'-19.8238889'},
    {'nombre':'SLPO', 'longitude':	'-65.7233333333' , 'latitude':	'19.5422222'},
    {'nombre':'SLTJ', 'longitude':	'-64.701302' , 'latitude':	'-21.5557'},
    {'nombre':'SLVM', 'longitude':	'-63.4066666666' , 'latitude':	'-21.2541667'},
    {'nombre':'SLYA', 'longitude':	'-63.65166666666' , 'latitude':	'-21.9608333'},
    
    {'nombre':'SLVR', 'longitude':	'-63.1353' , 'latitude':	'-17.644699'},
    {'nombre':'SLAS', 'longitude':	'-63.15666666666' , 'latitude':	'-15.9302778'},
    {'nombre':'SLCA', 'longitude':	'-63.5274999999' , 'latitude':	'-20.0072222'},
    {'nombre':'SLCP', 'longitude':	'-62.028611111' , 'latitude':	'-16.1383333'},
    {'nombre':'SLET', 'longitude':	'-63.171398' , 'latitude':	'-17.811501'},
    {'nombre':'SLSI', 'longitude':	'-60.96166666666' , 'latitude':	'-16.3844444'},
    {'nombre':'SLJV', 'longitude':	'-62.4702777777' , 'latitude':	'-16.2708333'},
    {'nombre':'SLJE', 'longitude':	'-60.7430555555' , 'latitude':	'-17.8308333'},
    {'nombre':'SLTI', 'longitude':	'-58.40194444444' , 'latitude':	'-16.3391667'},
    {'nombre':'SLRB', 'longitude':	'-59.7658333333' , 'latitude':	'-18.3277778'},
    {'nombre':'SLPS', 'longitude':	'-57.8191625744' , 'latitude':	'-18.9748221244'},
    {'nombre':'SLVG', 'longitude':	'-64.0994444444' , 'latitude':	'-18.4825'},
    {'nombre':'SLSV', 'longitude':	'-62.470556' , 'latitude':	'-16.266667'},
    
    {'nombre':'SLTR', 'longitude':	'-64.917999' , 'latitude':	'-14.8187'},
    {'nombre':'SLCO', 'longitude':	'-68.782778' , 'latitude':	'-11.040278'},
    {'nombre':'SLGM', 'longitude':	'-65.345802' , 'latitude':	'-10.8216'},
    {'nombre':'SLJO', 'longitude':	'-64.6744444444' , 'latitude':	'-13.0658333'},
    {'nombre':'SLMG', 'longitude':	'-64.0619444444' , 'latitude':	'-13.2586111'},
    {'nombre':'SLRI', 'longitude':	'-66.116669' , 'latitude':	'-11.0105'},
    {'nombre':'SLSA', 'longitude':	'-65.4347222222' , 'latitude':	'-13.7616667'},
    {'nombre':'SLSM', 'longitude':	'-65.6338888888' , 'latitude':	'-14.9655556'},
    {'nombre':'SLRA', 'longitude':	'-64.6038888888' , 'latitude':	'-13.2638889'},
    {'nombre':'SLSR', 'longitude':	'-66.7869444444' , 'latitude':	'-14.0744444'},
    
]

    //COLORES
    const color=[
        {'color':'#00CC00'},

        {'color':'#EED54C'},
        {'color':'#EED54C'},
        {'color':'#EED54C'},
        {'color':'#EED54C'},
        {'color':'#EED54C'},
        {'color':'#EED54C'},
        {'color':'#EED54C'},
        {'color':'#EED54C'},

        {'color':'#FF6633'},
        {'color':'#FF6633'},
        {'color':'#FF6633'},
        {'color':'#FF6633'},
        {'color':'#FF6633'},
        {'color':'#FF6633'},
        {'color':'#FF6633'},
        {'color':'#FF6633'},
        {'color':'#FF6633'},

        {'color':'#F76675'},
        {'color':'#F76675'},
        {'color':'#F76675'},
        {'color':'#F76675'},
        {'color':'#F76675'},
        {'color':'#F76675'},
        {'color':'#F76675'},
        {'color':'#F76675'},
        {'color':'#F76675'},
        {'color':'#F76675'},
        {'color':'#F76675'},
        {'color':'#F76675'},
        {'color':'#F76675'},

        {'color':'#0066CC'},
        {'color':'#0066CC'},
        {'color':'#0066CC'},
        {'color':'#0066CC'},
        {'color':'#0066CC'},
        {'color':'#0066CC'},
        {'color':'#0066CC'},
        {'color':'#0066CC'},
        {'color':'#0066CC'},
        {'color':'#0066CC'},
    ]  

    //MARCADORES

    for (let index = 0; index < dic.length; index++) {
        var marker = L.circleMarker([ dic[index].latitude, dic[index].longitude],{
            radius: 10,
            fillColor: color[index].color,
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8,
            //title: "test"}).addTo(map); /* .on('click', onClick) */
            title: "test"}).addTo(map).on('click', onClick);
            marker.myJsonData = dic[index].nombre;
        
        marker.bindTooltip(dic[index].nombre, {permanent:true});
        marker.bindPopup(dic[index].nombre).closePopup();

        //marker.on('click', onClick)

    }
    function onClick(e) {
        var icao = String(e.target.myJsonData);
        //alert("Ciudad: " + e.target.myJsonData + "___" + icao);
        componente.sw_c=true;
        componente.sw_a=true;
        componente.cambiando_titulo(icao);
        
        const path = 'https://upsilon.aasana.bo/icao_notam/' + '?airport='+icao;
        
        axios.get(path).then((respuesta) => {
        componente.recibiendo_datos_db( respuesta.data.lista_notam_charly, respuesta.data.lista_notam_alfa );
        }).catch((error) => {
        console.log(error)
        })
    }
}
initmap();