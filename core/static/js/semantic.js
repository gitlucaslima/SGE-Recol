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

    console.log(quantidade1)
    console.log(quantidade2)

    if(quantidade1 > quantidade2){
        minhadiv.style.display = "block";
        setTimeout(function() {
            $('minhadiv').fadeOut('slow');
        }, 1000);
    }
    
}