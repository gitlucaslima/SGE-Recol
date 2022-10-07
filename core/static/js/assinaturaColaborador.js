jQuery(document).ready(function($){
    var canvas = document.getElementById("signatureColaborador");
    var signaturePad = new SignaturePad(canvas);
    
    $('#clear-signature-colab').on('click', function(){
        signaturePad.clear();
    });

    var salvarColab = document.getElementById("saveColab")

    salvarColab.addEventListener("click", salvaColab)

    function salvaColab(){
        var assinatura = signaturePad.toDataURL();
        var btnsaveColab = document.getElementById("saveColab");

        //Elemento na página chamadora que será adicionado o valor da filho
        var assinaturaColaborador = window.document.getElementById("assinaturaColaborador");
        assinaturaColaborador.value = assinatura


        // Fechar modal dps do save
        btnsaveColab.setAttribute("data-bs-toggle","modal")
        btnsaveColab.click()
    }
    
});