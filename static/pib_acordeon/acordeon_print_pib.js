var componente = new Vue({
    el: "#appFormularioOaci",
    delimiters: ['[[', ']]'],
    vuetify: new Vuetify(),

    data: {
        heading: "Administración de Aeropuertos y \nServicios Auxiliares a la Navegación Aérea \nEstado Plurinacional de Bolivia",
        nombre_archivo: "",
    },
    methods: {
        generatePDF: function () {
            // Get HTML to print from element
            var prtHtml = document.getElementById('PIB').innerHTML;
            
            // Get all stylesheets HTML
            let stylesHtml = '';
            for (const node of [...document.querySelectorAll('link[rel="stylesheet"], style')]) {
                stylesHtml += node.outerHTML;
            }

            // Open the print window
            const WinPrint = window.open('', '', 'left=10,top=10,width=800,height=900,toolbar=0,scrollbars=1,status=0');

            const boton_print = '<button id="btn-eliminar" class="btn btn-success" onclick="print_page()">Imprimir PIB</button> <script> function print_page(){ if (window.print) {  document.getElementById("btn-eliminar").style.display="none"; window.print(); document.getElementById("btn-eliminar").style.display=""; } } </script>';
            WinPrint.document.write(`<!DOCTYPE html>
            <html>
            <head>
            ${stylesHtml}
            
                <style> 
                    @page {
                        margin-left: 1cm;
                        margin-right: 1cm;
                        margin-bottom: 1.5cm;
                    }
                    body {
                        margin: 0 !important;
                        background: white;
                    }
                </style>
            </head>
            <body>
                ${boton_print}
                ${prtHtml}
            </body>
            </html>`);
        }
    }
});