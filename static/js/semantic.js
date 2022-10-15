var cpf = document.getElementById("cpfColaborador");
var quanti = document.getElementById("quantidadeDisponivel");
var quantiUsuario = document.getElementById("quantidadeEquipamento");
var minhadiv = document.getElementById("minhaDiv");
var quantiRequirida = document.getElementById("quantidadeEquipamento");
var btnCancelar = document.getElementById("btnCancelar");
var drop = document.getElementById("dropdownEquip");
var checkbox = document.getElementById("flexSwitchCheckChecked")
var divinput = document.getElementById("divDate")
var inputDate = document.getElementById("inputDate")
var iconeColab = document.getElementById("iconeColab")
var iconeRespo = document.getElementById("iconeRespo")
var assinaturaResponsavel = document.getElementById("assinaturaResponsavel")
var assinaturaColaborador = document.getElementById("assinaturaColaborador")

console.log(assinaturaResponsavel)
console.log(assinaturaColaborador)



function carregarInput(){
    console.log(checkbox)
    if(checkbox.checked){
        divinput.style.display = "none";
        inputDate.removeAttribute("required")

    }
    else{
        divinput.style.display = "block";
        inputDate.setAttribute("required", "")
        console.log(inputDate)

    }
}

checkbox.addEventListener('change', carregarInput)

minhadiv.style.display = "none";

btnCancelar.addEventListener("click", function (a) {
    var colab = document.getElementById("colab");
    var respo = window.document.getElementById("respo");

    colab.src = "https://st2.depositphotos.com/5007459/8489/v/450/depositphotos_84895786-stock-illustration-writing-hand.jpg"
    respo.src = "https://st2.depositphotos.com/5007459/8489/v/450/depositphotos_84895786-stock-illustration-writing-hand.jpg"
    minhadiv.style.display = "none";
    cpf.setAttribute("value", "");
});

function changeHiddenInput (objDropDown)
{
   var colab = document.getElementById("hiddenInput").value = objDropDown.value;
   cpf.setAttribute("value", colab);
}

function changeHiddenInputEquip (objDropDown)
{  
   var texto = $('#dropdownEquip :selected').text();
   var nomeEquipamento = document.getElementById("nomeEquipamento");
   var equip = document.getElementById("hiddenInputEquip").value = objDropDown.value;

   quanti.setAttribute("value", equip);
   nomeEquipamento.setAttribute("value", texto)

}

quantiRequirida.addEventListener('change', updateValue);

function updateValue() {
    var quantidade1 = Number(quantiRequirida.value);
    var quantidade2 = Number(quanti.value);

    if(quantidade1 > quantidade2){
        minhadiv.style.display = "block";
        setTimeout(function() {
            $('minhadiv').fadeOut('slow');
        }, 1000);
    }
    
}
