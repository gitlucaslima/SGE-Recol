jQuery(document).ready(function($){
    var canvas = document.getElementById("signatureResponsavel");
    var signaturePad = new SignaturePad(canvas);

    function isCanvasBlank(canvas) {
        const context = canvas.getContext('2d');
      
        const pixelBuffer = new Uint32Array(
          context.getImageData(0, 0, canvas.width, canvas.height).data.buffer
        );
      
        return !pixelBuffer.some(color => color !== 0);
    }
    
    $('#clear-signature-respo').on('click', function(){
        signaturePad.clear();
    });

    var salvarRespo = document.getElementById("saveRespo")

    salvarRespo.addEventListener("click", salvaRespo)

    function salvaRespo(){
        const blank = isCanvasBlank(document.getElementById('signatureResponsavel'));

        if(blank){
            alert('Por favor forneça uma assinatura');
        }
        else{
            var assinatura = signaturePad.toDataURL();
            var btnsaveRespo = document.getElementById("saveRespo");

            //Elemento na página chamadora que será adicionado o valor da filho
            var assinaturaResponsavel = window.document.getElementById("assinaturaResponsavel");
            console.log(assinaturaResponsavel)
            var respo = window.document.getElementById("respo");
            
            assinaturaResponsavel.value = assinatura
            respo.src = assinatura;

            // Fechar modal dps do save
            btnsaveRespo.setAttribute("data-bs-toggle","modal")
            btnsaveRespo.click()
        }
    }
    
});