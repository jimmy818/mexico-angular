import { Inject, Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, filter, switchMap, take } from 'rxjs/operators';

import { AuthService } from '../services/auth.service';
import { SP_CORE_CONFIG } from '../sp-core.constants';
import { SpCoreConfig } from '../sp-core-config.interface';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  private isRefreshing = false;
  private refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

  constructor(
    @Inject(SP_CORE_CONFIG) private config: SpCoreConfig,
    private authService: AuthService,
  ) { }

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {

    // Omite las solicitudes generadas por carga de imágenes mediante MatIconRegistry.
    if (request.url.includes("assets") || request.url.includes("token/")) {
      return next.handle(request);
    }

    const url = `${this.config.apiBaseUrl}${request.url}`.replace(/([^:]\/)\/+/g, '$1');
    request = request.clone({ url });

    // Si el usuario está autenticado entonces se agrega el encabezado de autenticación
    const token = this.authService.getToken();
    if (token) {
      request = this.addToken(request, token);
    }

    return next.handle(request)
      .pipe(
        // Error en solicitudes http
        catchError(error => {
          if (error instanceof HttpErrorResponse && error.status === 401) {
            return this.handle401Error(request, next);
          } else {
            return throwError(error);
          }
        })
      );
  }

  private handle401Error(request: HttpRequest<any>, next: HttpHandler) {
    if (!this.isRefreshing) {
      // Si no existe una solicitud de refresh previa se solicita.
      this.isRefreshing = true;
      this.refreshTokenSubject.next(null);
      return this.authService
        .refreshToken()
        .pipe(
          switchMap(access => {
            this.isRefreshing = false;
            this.refreshTokenSubject.next(access);
            // Agrega el token de autenticación obtenido mediante el refresh token.
            return next.handle(this.addToken(request, access));
          }),
          catchError(error => {
            // Si ocurre algún error con la obtención del refresh token se envía a cerrar sesión
            this.authService.logout();
            return throwError(error);
          }));

    } else {
      // Si existe una solicitud previa de refresh previa se espera su respuesta.
      return this.refreshTokenSubject
        .pipe(
          filter(token => token != null),
          take(1),
          switchMap(access => {
            // Agrega el token de autenticación obtenido mediante el refresh token previo.
            return next.handle(this.addToken(request, access));
          }));
    }
  }

  /**
   * Agrega encabezado de autenticación
   */
  private addToken(request: HttpRequest<any>, token: string) {
    return request.clone({
      setHeaders: {
        'Authorization': `Bearer ${token}`
      }
    });
  }
}
