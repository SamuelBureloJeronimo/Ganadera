import { AfterViewInit, Component } from '@angular/core';
import { lastValueFrom } from 'rxjs';
import Swal from 'sweetalert2'

// IMPORTACIÓN DE MODULOS
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { GeneralService } from '../../services/general.service';
import { CookieService } from 'ngx-cookie-service';

// IMPORTACIÓN DE SERVICIOS
@Component({
  selector: 'app-login',
  imports: [MatIconModule, RouterModule, CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  //Almacena el nombre de usuario ingresado por el usuario.
  public email: string = "";
  //Almacena la contraseña ingresada por el usuario.
  public password: string = "";

  /**
   * Inyecta dependencias necesarias para el componente.
   *
   * @param genServ -> Instancia del servicio ClienteService para realizar la autenticación del usuario.
   * @param _router -> Instancia del servicio de enrutamiento Angular para redirigir al usuario después del inicio de sesión exitoso.
   */
  constructor(private _router: Router, private cookieServ: CookieService) {
    this.email = "user_dsfsdvesservc";
    this.password = "1415";
    this.cookieServ.delete("token");
  }


  //Maneja la lógica cuando el usuario envía el formulario de inicio de sesión.
  async onSubmit() {
    //Verifica que ambos campos, username y password, no estén vacíos.

    if (this.email && this.password) {
      //Crea un objeto formData con las credenciales del usuario.
      let form = new FormData();
      form.set("email", this.email);
      form.set("password", this.password);
      /*
      try {
        //Realiza una solicitud de inicio de sesión a través del método login del servicio ClienteService.
        let res = await lastValueFrom(this.genServ.login(form));

        //Almacena el token de acceso
        this.cookieServ.set("token", res.token);

        let nextRoute = "/dashboard";

        switch(res.rol) {
          case "0":
            nextRoute += "/client/my-consume";
            break;
          case "1":
            nextRoute += "/capturist/register-client";
            break;
          case "2":
              nextRoute += "/technician/register-device";
              break;
          case "3":
            nextRoute += "/admin/register-user";
            break;
          case "4":
            nextRoute += "/owner/my-company";
            break;
          case "5":
            nextRoute += "/superuser/metrics";
            break;
          default:
            Swal.fire(
              'Error...', 'El rol proporcionado no existe', 'error'
            );
            break;
        }
        this._router.navigate([nextRoute]);
      } catch (error: any) {
        //Si ocurre un error durante la autenticación:
        console.log(error);
        if (error.status == 401) {
          Swal.fire(
            'Datos invalidos',
            'El usuario o contraseña son invalidos',
            'error'
          );
        } else {
          //Muestra una alerta utilizando Swal.fire con un mensaje de error.
          Swal.fire(
            'Error externo',
            'Algo paso al intentar validar tus credenciales, intentalo más tarde.',
            'error'
          );
          }
        }*/

    } else {
      alert('Por favor, ingrese usuario y contraseña');
    }
  }
}
