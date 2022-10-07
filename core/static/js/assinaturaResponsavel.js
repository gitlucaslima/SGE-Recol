jQuery(document).ready(function($){
    var canvas = document.getElementById("signatureResponsavel");
    var signaturePad = new SignaturePad(canvas);
    
    $('#clear-signature-respo').on('click', function(){
        signaturePad.clear();
    });

    var salvarRespo = document.getElementById("saveRespo")

    salvarRespo.addEventListener("click", salvaRespo)

    function salvaRespo(){
        var assinatura = signaturePad.toDataURL();
        var btnsaveRespo = document.getElementById("saveRespo");

        //Elemento na página chamadora que será adicionado o valor da filho
        var assinaturaResponsavel = window.document.getElementById("assinaturaResponsavel");
        assinaturaResponsavel.value = assinatura

        // Fechar modal dps do save
        btnsaveRespo.setAttribute("data-bs-toggle","modal")
        btnsaveRespo.click()
    }
    
});