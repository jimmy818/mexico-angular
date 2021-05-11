/**
 * ==================================================================
 * Referencias:
 * https://angular-academy.com/angular-jwt/
 * ==================================================================
 */

import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { tap, catchError, map, mapTo } from 'rxjs/operators';
import * as moment_ from 'moment';
const moment = moment_;

import { SP_CORE_CONFIG } from '../sp-core.constants';
import { Gender } from '../models/enums/gender.enum';
import { UserType } from '../models/enums/user-type.enum';
import { UserInfo } from '../models/interfaces/user-info.interface';
import { SpCoreConfig } from '../sp-core-config.interface';

import { LocalStorageService } from './local-storage.service';
import { tokenResponse } from '../models/interfaces/token-response.interface';
import { UserInfoResponse } from '../models/interfaces/user-info-response.interface';
import { ForgotPasswordResponse } from '../models/interfaces/forgot-password-response.interface';
import { ForgotPassword } from '../models/interfaces/forgot-password.interface';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly TOKEN_KEY = 'TOKEN';
  private readonly REFRESH_TOKEN_KEY = 'REFRESH_TOKEN';
  private readonly USERNAME = 'USERNAME';
  private readonly INSTITUTION_ID = 'INSTITUTION_ID';

  /**
   * Obtiene o establece el nombre de usuario autenticado.
   */
  get userAuthenticated(): string {
    return this.lsService.get(this.USERNAME);
  }
  set userAuthenticated(username: string) {
    if (username === null) {
      this.lsService.remove(this.USERNAME);
    } else {
      this.lsService.set(this.USERNAME, username);
    }
  }

  /**
   * Obtiene o establece la institución del usuario autenticado.
   */
  get institutionId(): number {
    return +this.lsService.get(this.INSTITUTION_ID);
  }
  set institutionId(institutionId: number) {
    if (institutionId === null) {
      this.lsService.remove(this.INSTITUTION_ID);
    } else {
      this.lsService.set(this.INSTITUTION_ID, institutionId.toString());
    }
  }

  constructor(
    @Inject(SP_CORE_CONFIG) private config: SpCoreConfig,
    private http: HttpClient,
    private lsService: LocalStorageService,
  ) { }

  /**
   * Inicia sesión del usuario
   * @param apiBaseUrl Url base del API
   * @param username Nombre de usuario
   * @param password Contraseña del usuario
   */
  login(
    username: string,
    password: string
  ): Observable<boolean> {

    const tokenUrl = this.config.tokenUrl || 'token/';

    const params = new HttpParams()
      .set('email', username)
      .set('password', password);

    return this.http
      .post<tokenResponse>(`${this.config.apiBaseUrl}${tokenUrl}`, params)
      .pipe(
        tap(user => {
          // Almacena el nombre de usuario autenticado.
          this.userAuthenticated = username;
          // Almacena la institución del usuario autenticado.
          this.institutionId = user.institution;
          // Almacena los tokens (token, refresh token).
          this.storeTokens(user.access, user.refresh);
        }),
        mapTo(true),
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }));
  }

  /**
   * Obtiene la clave de refresh token en caso de caducidad de la clave token
   */
  refreshToken(): Observable<string> {

    const refreshTokenUrl = this.config.refreshTokenUrl || 'token-refresh/';

    const params = new HttpParams()
      .set('refresh', this.getRefreshToken());

    return this.http
      .post<any>(`${this.config.apiBaseUrl}${refreshTokenUrl}`, params)
      .pipe(
        tap(result => {
          this.setToken(result.access);
        }),
        map(result => result.access),
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }));
  }

  /**
   * Obtiene información del usuario autenticado.
   */
  getUserInfo(): Observable<UserInfo> {

    const userInfoUrl = this.config.userInfoUrl || 'me';
    return this.http
      .get<UserInfoResponse>(userInfoUrl)
      .pipe(
        map(userInfoResponse => {
          // TODO: Investigar una manera automática para realizar el mapeo mediante decoradores.
          return <UserInfo>{
            id: userInfoResponse.id,
            type: <UserType>userInfoResponse.type,
            region: userInfoResponse.region,
            fullName: userInfoResponse.full_name,
            countryCode: userInfoResponse.country_code,
            phone: userInfoResponse.phone,
            gender: <Gender>userInfoResponse.gender,
            birthdate: moment(userInfoResponse.birthday).toDate(),
            photo: userInfoResponse.phone,
            email: userInfoResponse.email,
            teamId: userInfoResponse.team,
            institutionId: userInfoResponse.institution,
            username: userInfoResponse.username,
            emailVerified: userInfoResponse.email_verified,
            isSubscriptionActive: userInfoResponse.subscription_active,
            isActive: userInfoResponse.is_active
          };
        }),
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }));
  }

  /**
   * Envía correo para recuperación o restablecimiento de contraseña
   */
  forgotPassword(
    email: string
  ): Observable<ForgotPassword> {

    const forgotPasswordUrl = this.config.forgotPasswordUrl || 'reset-password/';

    const params = new HttpParams()
      .set('email', email);

    return this.http
      .post<ForgotPasswordResponse>(forgotPasswordUrl, params)
      .pipe(
        map(response => {
          return <ForgotPassword>{
            email: response.email
          }
        }),
        catchError((error: HttpErrorResponse) => {
          return throwError(error);
        }));
  }

  /**
   * Cierra sesión.
   * TODO: Confirmar si existe servicio para cerrar sesión
   */
  logout(): Observable<boolean> {
    // Elimina dato de nombre de usuario en sesión.
    this.userAuthenticated = null;
    // Elimina dato de institución.
    this.institutionId = null;
    // Elimina registro de autenticación.
    this.removeTokens();
    return of(true);
  }

  /**
   * Verifica si el usuario está autenticado. 
   * Cuando se tenga almacenado el token entonces el usuario está autenticado.
   */
  isUserAuthenticated(): boolean {
    return !!this.getToken();
  }

  /**
   * Obtiene el token de autenticación
   */
  getToken(): string {
    return this.lsService.get(this.TOKEN_KEY);
  }

  /**
   * Obtiene el refresh token de autenticación almacenado en el login
   */
  getRefreshToken(): string {
    return this.lsService.get(this.REFRESH_TOKEN_KEY);
  }

  /**
   * Almacena token de autenticación
   * @param token Token de autenticación
   */
  private setToken(token: string) {
    this.lsService.set(this.TOKEN_KEY, token);
  }

  /**
   * Almacena refresh token de autenticación
   * @param refreshToken Refresh token de autenticación
   */
  private setRefreshToken(refreshToken: string) {
    this.lsService.set(this.REFRESH_TOKEN_KEY, refreshToken);
  }

  /**
   * Almacena las claves de token y refresk token
   * @param token Token de autenticación
   * @param refreshToken Refresh token de autenticación
   */
  private storeTokens(token: string, refreshToken: string): void {
    this.setToken(token);
    this.setRefreshToken(refreshToken);
  }

  /**
   * Elimina las claves de token y refresh token
   */
  private removeTokens(): void {
    this.lsService.remove(this.TOKEN_KEY);
    this.lsService.remove(this.REFRESH_TOKEN_KEY);
  }
}
