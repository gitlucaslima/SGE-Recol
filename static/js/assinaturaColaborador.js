jQuery(document).ready(function($){
    var canvas = document.getElementById("signatureColaborador");
    var signaturePad = new SignaturePad(canvas);

    function isCanvasBlank(canvas) {
        const context = canvas.getContext('2d');
      
        const pixelBuffer = new Uint32Array(
          context.getImageData(0, 0, canvas.width, canvas.height).data.buffer
        );
      
        return !pixelBuffer.some(color => color !== 0);
    }
    
    $('#clear-signature-colab').on('click', function(){
        signaturePad.clear();
    });

    var salvarColab = document.getElementById("saveColab")

    salvarColab.addEventListener("click", salvaColab)

    function salvaColab(){
        const blank = isCanvasBlank(document.getElementById('signatureColaborador'));

        if(blank){
            alert('Por favor forneça uma assinatura');
        }
        else{
            var assinatura = signaturePad.toDataURL();
            var btnsaveColab = document.getElementById("saveColab");

            //Elemento na página chamadora que será adicionado o valor da filho
            var assinaturaColaborador = window.document.getElementById("assinaturaColaborador");
            console.log(assinaturaColaborador)
            var colab = window.document.getElementById("colab");

            assinaturaColaborador.value = assinatura
            colab.src = assinatura

            // Fechar modal dps do save
            btnsaveColab.setAttribute("data-bs-toggle","modal")
            btnsaveColab.click()
        }
    }
    
});