(function(){

    // Solicitamos variables del html

    var btn1 = document.getElementById("btn-desplegar"),
        btn2 = document.getElementById("btn-cerrar"),
        form = document.getElementById("formularioClientes");

    function desplegar(e){
        form.style.display = 'block';
        btn1.style.display = 'none';
        btn2.style.display = 'block';
        btn1.removeEventListener('click',desplegar);
        btn2.addEventListener('click',cerrar);
        e.preventDefault();
    }

    function cerrar(e){
        btn1.style.display = 'block';
        btn2.style.display = 'none';
        form.style.display = 'none';
        btn1.addEventListener('click',desplegar);
        e.preventDefault();
    }

    btn1.addEventListener('click',desplegar);

}());