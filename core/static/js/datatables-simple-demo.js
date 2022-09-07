window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple,{
            language: {
                url: "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese.json"
            }
        });
        
    }
});
