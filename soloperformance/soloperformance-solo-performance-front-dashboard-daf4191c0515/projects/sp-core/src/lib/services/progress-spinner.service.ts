import { Injectable } from '@angular/core';
import { iif, Observable, of, Subject } from 'rxjs';
import { delay, switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ProgressSpinnerService {

  /**
   * Indicador de ejecución del control de progreso
   */
  public stateChange = new Subject<boolean>();

  /**
   * Texto descriptivo del proceso en ejecución.
   */
  public text = '';

  /**
   * Tiempo de espera antes de iniciar el control de progreso. Por defecto inmediato.
   */
  public delay = 0;

  /**
   * Tiempo de espera actual.
   */
  private currentTimeOut: any;


  /**
   * Inicia el control de progreso.
   */
  public start(text = ''): void {

    // Si ya se indicó iniciar pero aún está en el tiempo de espera (delay) no realiza ninguna acción.
    if (this.currentTimeOut) {
      return;
    }

    // Se inicia el control de progreso, después del tiempo de espera indicado.
    this.currentTimeOut = setTimeout(() => {
      this.text = text;
      this.stateChange.next(true);
      this.cancelTimeOut();
    }, this.delay);
  }

  /**
   * Detiene el control de progreso.
   */
  public stop(): void {
    this.cancelTimeOut();
    this.stateChange.next(false);
  }

  /**
   * Obtiene un objeto observable para control de progreso. 
   * Para permitir visualizar un control de progreso después de cierto tiempo de espera.
   * @param delayMilliseconds Milisegundos de espera
   */
  public isLoadingSubject(
    subject: Subject<boolean>,
    delayMilliseconds = 500
  ): Observable<boolean> {
    return subject.pipe(
      switchMap(loading =>
        iif(() => loading,
          of(loading).pipe(delay(delayMilliseconds)),
          of(loading)
        )
      )
    );
  }

  /**
   * Cancela el tiempo de espera.
   */
  private cancelTimeOut() {
    clearTimeout(this.currentTimeOut);
    this.currentTimeOut = null;
  }
}
