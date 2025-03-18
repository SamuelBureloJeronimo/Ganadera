function addSwalAlert(id, endpoint, url_redir){
    document.getElementById(id).addEventListener("submit", function(event) {
      event.preventDefault();  // Evita que la página se recargue

      let formData = new FormData(this);

      fetch(endpoint, {
          method: "POST",
          body: formData
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
            window.location.href = url_redir;  // Redirige a otra página
          } else {
              Swal.fire({
                  title: "Usuario o contraseña incorrecto",
                  text: data.message,
                  icon: "info"
              });
          }
      });
  });
}

function logOut(){
    window.location.href = "/";  // Redirige a otra página
}