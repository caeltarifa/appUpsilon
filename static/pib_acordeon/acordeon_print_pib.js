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
            const prtHtml = document.getElementById('PIB').innerHTML;

            // Get all stylesheets HTML
            let stylesHtml = '';
            for (const node of [...document.querySelectorAll('link[rel="stylesheet"], style')]) {
                stylesHtml += node.outerHTML;
            }

            // Open the print window
            const WinPrint = window.open('', '', 'left=0,top=0,width=800,height=900,toolbar=0,scrollbars=0,status=0');

            WinPrint.document.write(`<!DOCTYPE html>
            <html>
            <head>
                ${stylesHtml}
                <style> background: white;</style>
            </head>
            <body>
                ${prtHtml}
            </body>
            </html>`);
        }
    }
});