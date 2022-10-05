var cpf = document.getElementById("cpfColaborador");
var quanti = document.getElementById("quantidadeDisponivel");
var quantiUsuario = document.getElementById("quantidadeEquipamento");
var minhadiv = document.getElementById("minhaDiv");
var quantiRequirida = document.getElementById("quantidadeEquipamento");
var btnCancelar = document.getElementById("btnCancelar")

minhadiv.style.display = "none";

var dataString = $("form").serialize();

btnCancelar.addEventListener("click", function () {
    minhadiv.style.display = "none";
});

function changeHiddenInput (objDropDown)
{
   var colab = document.getElementById("hiddenInput").value = objDropDown.value;
   cpf.setAttribute("value", colab);
}

function changeHiddenInputEquip (objDropDown)
{
   var equip = document.getElementById("hiddenInputEquip").value = objDropDown.value;
   quanti.setAttribute("value", equip);
}

// quantiRequirida.addEventListener('change', updateValue);

// function updateValue(e) {
//     var quantidade1 = Number(quantiRequirida.value);
//     var quantidade2 = Number(quanti.value);

//     console.log(quantidade1)
//     console.log(quantidade2)

//     if(quantidade1 > quantidade2){
//         minhadiv.style.display = "block";
//         setTimeout(function() {
//             $('minhadiv').fadeOut('slow');
//         }, 3000);
//     }
    
// }