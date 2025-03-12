import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';

export interface JwtPayloadUser {
  email: string;
  id_company: string;
  sub: string;
}

@Injectable({
  providedIn: 'root',
})
export class GeneralService {
  public url_server: string;
  /**
   * La función constructora inicializa el HttpClient y establece los valores de URL y token.
   * @param {HttpClient} _http - El parámetro `_http` es de tipo `HttpClient`,
   * que es un servicio proporcionado por Angular para realizar peticiones HTTP a un servidor. Permite
   * enviar peticiones GET, POST, PUT, DELETE, etc. a un servidor backend y manejar las respuestas.
   */
  constructor(public _http: HttpClient, private cookie: CookieService) {
    this.url_server = 'http://localhost:5000';
  }
  public init_dashboard(): Observable<any> {
    return this._http.get(this.url_server + '/init-dashboard', {
      headers: this.headerToken(),
    });
  }
  public isAuth(): Observable<any> {
    return this._http.get(this.url_server + '/auth-token', {
      headers: this.headerToken(),
    });
  }
  public login(fomData: any): Observable<any> {
    return this._http.post(this.url_server + '/login', fomData);
  }
  public sendEmail(mail: string, form: any): Observable<any> {
    return this._http.post(this.url_server + '/enviar_usuario/' + mail, form, {
      headers: this.headerToken(),
    });
  }
  public get_paises(): Observable<any> {
    return this._http.get(this.url_server + '/get-paises');
  }
  public get_estados(id_pais: number): Observable<any> {
    return this._http.get(this.url_server + '/get-estados/' + id_pais);
  }
  public get_municipios(id_estado: number): Observable<any> {
    return this._http.get(this.url_server + '/get-municipios/' + id_estado);
  }
  public get_colonias(id_colonias: number): Observable<any> {
    return this._http.get(this.url_server + '/get-colonias/' + id_colonias);
  }
  public get_colonias_by_cp(cp: number): Observable<any> {
    return this._http.get(this.url_server + '/get-colonias-by-cp/' + cp);
  }
  public getIPAddress(): Observable<any> {
    return this._http.get('http://api.ipify.org/?format=json');
  }
  public getMetrics(): Observable<any> {
    return this._http.get(this.url_server + '/api/v1/get-metrics');
  }
  public getToken(): string {
    return this.cookie.get('token');
  }
  public registerVisit() {
    // MODULO PARA MEDIR EL TIEMPO DE CARGA DE LA PÁGINA
    let endTime = performance.now();
    let startTime = parseFloat(this.cookie.get('*AuthTime'));
    let loadTime = endTime - startTime;
    this.cookie.set('--TimeCharge-After', this.cookie.get('--TimeCharge-This'));
    this.cookie.set(
      '--TimeCharge-This',
      (loadTime / 1000).toFixed(4).toString()
    );
    // -------- ---------- ---------
    let data = {
      't-carga': this.cookie.get('--TimeCharge-After'),
      ip: this.cookie.get('ip'),
      't-page': this.cookie.get('TimeInPage'),
      userAgent: this.cookie.get('userAgent'),
      url: this.cookie.get('url'),
      token: '',
    };
    let form = new FormData();
    form.set(
      't-carga',
      parseFloat(this.cookie.get('--TimeCharge-After')).toFixed(2)
    );
    form.set('ip', this.cookie.get('ip').toString());
    form.set('t-page', parseFloat(this.cookie.get('TimeInPage')).toFixed(2));
    form.set('userAgent', this.cookie.get('userAgent'));
    form.set('url', this.cookie.get('url').toString());

    let tok = this.cookie.get('token');
    if (tok != undefined) {
      form.set('token', this.cookie.get('token'));
      data['token'] = this.cookie.get('token');
    }
    console.log(form.get('t-carga'));

    let tiempo_carga = form.get('t-carga');

    if (Number.isNaN(Number(tiempo_carga))) {
      console.log('Es NaN');
      return; // Si es NaN, retorna y no sigue ejecutando
    }

    this.register_visit(form).subscribe(
      (res: any) => {
        console.log(res);
      },
      (error: any) => {
        console.log(error);
      }
    );
  }

  public register_visit(form: any): Observable<any> {
    return this._http.post(this.url_server + '/api/v1/visit', form);
  }

  public headerToken(): HttpHeaders {
    let token = this.cookie.get('token');
    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
  }
}
