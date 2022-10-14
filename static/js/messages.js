const botao = document.getElementsByClassName('btn-close');
console.log(botao); // 👉️ [div.box, div.box, div.box]

// ✅ addEventListener to first box
botao[0].addEventListener('click', function onClick() {
    console.log('botao clicado');

    const aviso = document.getElementsByClassName('alert')
    aviso[0].remove()

});