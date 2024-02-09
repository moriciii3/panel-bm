(function(){

    // Desplegar la barra lateral responsive

    var btnDesplegar = document.getElementById("btn-nav-desplegar"),
        btnCerrar = document.getElementById("btn-nav-cerrar"),
        barra = document.getElementById("barraLateral");

    function desplegar(e){
        barra.style.display = 'block';
        barra.style.width = "30%";
        barra.style.position = "absolute";
        btnDesplegar.style.display = 'none';
        btnCerrar.style.display = 'block';
        btnCerrar.addEventListener('click',cerrar);
        e.preventDefault();
    }

    function cerrar(e){
        barra.style.display = 'none';
        btnDesplegar.style.display = 'block';
        btnCerrar.style.display = 'none';
        btnDesplegar.addEventListener('click',desplegar);
        e.preventDefault();
    }

    btnDesplegar.addEventListener('click',desplegar);

}());