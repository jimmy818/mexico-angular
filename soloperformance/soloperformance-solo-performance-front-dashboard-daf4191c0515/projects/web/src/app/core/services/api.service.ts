import { Injectable } from '@angular/core';
import { HttpClient, HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpResponse, HttpParams, HttpErrorResponse } from '@angular/common/http'
import { map, tap, catchError } from 'rxjs/operators';
import { Observable, throwError } from 'rxjs';
import { ErrorService } from './error.service';
import { LoaderService } from './loader.service';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private httpClient: HttpClient) { }

  get<T>(url: string, params?: HttpParams) {
    return this.httpClient.get<T>(url, { params: params })
  }

  post(url: string, data: any) {
    return this.httpClient.post(url, data)
  }

  patch(url: string, data: any) {
    return this.httpClient.patch(url, data)
  }

  put(url: string, data: any) {
    return this.httpClient.put(url, data)
  }

  delete(url: string) {
    return this.httpClient.delete(url)
  }

}

// intercepta las llamadas a los endpoits para setear el token
@Injectable() export class HttpConfigInterceptor implements HttpInterceptor {

  constructor(private err: ErrorService, private loader: LoaderService) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    return next.handle(req).pipe(
      map((event: HttpEvent<any>) => {
        if (event instanceof HttpResponse) {
          // console.log('event--->>>', event);
          this.loader.stop(1000);
        }
        return event;
      }),
      catchError((err: HttpErrorResponse) => {
        this.err.checkError(err);
        return throwError(err);
      })
    );
  }

}
