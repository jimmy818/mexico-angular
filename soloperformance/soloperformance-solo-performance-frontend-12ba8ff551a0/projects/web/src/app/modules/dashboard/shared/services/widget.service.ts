import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { map, mapTo } from 'rxjs/operators';

import { RequestParam, REQUEST_PARAM_NAMES } from 'sp-core';

import { UserWidget } from '../models/interfaces/user-widget.interface';
import { WidgetType } from '../models/enums/widget-type.enum';
import { Widget } from '../models/interfaces/widget.interface';
import { WidgetsResponse } from '../models-dto/widgets-response.interface';
import { UserWidgetsResponse } from '../models-dto/user-widgets-response.interface';
import { UserWidgetResponse } from '../models-dto/user-widget-response.interface';

@Injectable({
  providedIn: 'root'
})
export class WidgetService {

  private widgetAddRequestedSubject$ = new Subject<Widget>();
  /**
   * Observable para saber cuando se solicita crear un nuevo widget
   */
  widgetAddRequested$ = this.widgetAddRequestedSubject$.asObservable();

  private widgetDuplicateRequestedSubject$ = new Subject<Widget>();
  /**
   * Observable para saber cuando se solicita duplicar un widget
   */
  widgetDuplicateRequested$ = this.widgetDuplicateRequestedSubject$.asObservable();


  private userWidgetRemoveRequestedSubject$ = new Subject<number>();
  /**
   * Observable para saber cuando se solicita crear un nuevo widget
   */
  userWidgetRemoveRequested$ = this.userWidgetRemoveRequestedSubject$.asObservable();

  private userWidgetAddedSubject$ = new Subject<UserWidget>();
  /**
   * Observable para saber cuando un nuevo widget de usuario ha sido agregado.
   */
  userWidgetAdded$ = this.userWidgetAddedSubject$.asObservable();

  latestUserWidgetRemoved = 0;
  private userWidgetRemovedSubject$ = new BehaviorSubject<number>(this.latestUserWidgetRemoved);
  /**
   * Observable para saber cuando un widget de usuario ha sido eliminado.
   */
  userWidgetRemoved$ = this.userWidgetRemovedSubject$.asObservable();

  constructor(
    private http: HttpClient
  ) { }

  /**
   * Obtiene los widget existentes en sistema
   * @param params Parámetros de búsqueda
   */
  getWidgets(
    params?: Array<RequestParam>
  ): Observable<Array<Widget>> {

    // Filtros o parámetros.
    let httpParams = new HttpParams();
    if (params) {
      params.forEach(filter => {
        httpParams = httpParams.set(filter.key, filter.value);
      });
    }

    const options = {
      params: httpParams
    }

    return this.http
      .get<WidgetsResponse>('widget/', options)
      .pipe(
        map((response) => {
          // Convierte la información obtenida a un modelo más adecuado para procesamiento
          const widgets: Array<Widget> = [];
          id: response.data.forEach(widgetDto => {
            widgets.push(<Widget>{
              type: widgetDto.id,
              name: widgetDto.name,
              image: widgetDto.image,
              size: this.getWidgetSize(widgetDto.id),
            });
          });
          return widgets;
        })
      );
  }

  /**
   * Obtiene la lista de widget configurados del usuario en sesión.
   */
  getUserWidgets(): Observable<Array<UserWidget>> {

    let httpParams = new HttpParams()
      .set(REQUEST_PARAM_NAMES.sort, 'order');

    const options = {
      params: httpParams
    };

    return this.http.get<UserWidgetsResponse>('current-widgets/', options)
      .pipe(
        map((response) => {
          // Convierte la información obtenida a un modelo más adecuado para procesamiento
          const widgets: Array<UserWidget> = [];
          id: response.data.forEach(widgetResponse => {
            widgets.push(this.mapUserWidgetResponseToModel(widgetResponse));
          });
          return widgets;
        }));
  }

  /**
   * Agrega/configura un widget al usuario en sesión
   * @param widget Widget a agregar
   * @param axisX Posición X de ordenamiento
   * @param axisY Posición Y de ordenamiento
   */
  addWidgetToUser(
    widget: Widget,
    axisX: number,
    axisY: number
  ): Observable<UserWidget> {

    const body = {
      widget: widget.type,
      axis_x: axisX,
      axis_y: axisY
    };

    return this.http.post<UserWidgetResponse>('current-widgets/', body).pipe(
      map((response) => {
        const userWidget = this.mapUserWidgetResponseToModel(response);
        // Notifica que se ha agregado un nuevo widget al usuario.
        this.userWidgetAddedSubject$.next(userWidget);
        return userWidget;
      })
    );
  }

  /**
   * Elimina/ desasigna un widget del usuario en sesión
   * @param widgetId Widget a eliminar
   */
  removeWidgetFromUser(
    widgetId: number
  ): Observable<boolean> {
    return this.http
      .delete(`current-widgets/${widgetId.toString()}/`)
      .pipe(
        map(() => {
          this.latestUserWidgetRemoved = widgetId;
          this.userWidgetRemovedSubject$.next(widgetId);
          return true;
        })
      );
  }

  /**
   * Actualiza la información de la asignación del widget del usuario en sesión
   * @param userWidget Datos del widget de usuario
   */
  updateWidgetUser(
    userWidget: UserWidget
  ): Observable<boolean> {

    const body = {
      axis_x: userWidget.axisX,
      axis_y: userWidget.axisY
    };

    return this.http
      .patch(`current-widgets/${userWidget.id.toString()}/`, body)
      .pipe(
        mapTo(true)
      );
  }

  requestAddWidgetToUser(widget: Widget): void {
    this.widgetAddRequestedSubject$.next(widget);
  }

  requestDuplicateWidgetFromUser(widget: Widget): void {
    this.widgetDuplicateRequestedSubject$.next(widget);
  }

  requestRemoveWidgetFromUser(widgetId: number): void {
    this.userWidgetRemoveRequestedSubject$.next(widgetId);
  }

  /**
   * Obtiene el tamaño en columnas que corresponde según el tipo de widget. El tamaño total se considera que son 12 columnas.
   * @param type Tipo de widget
   */
  getWidgetSize(type: WidgetType): number {
    switch (type) {
      case WidgetType.teamList:
        return 3;
      case WidgetType.athleteList:
        return 3;
      case WidgetType.athletesCalendar:
        return 6;
      case WidgetType.teamsCalendar:
        return 6;
      case WidgetType.mainWidget:
        return 12;
      default:
        return 12;
    }
  }

  /**
   * Mapea la estructura de un widget de usuario obtenido de una solicitud http a estrcutura de modelo
   * @param response Widget de usuario en estructura devuelta por solicitudes http
   */
  private mapUserWidgetResponseToModel(response: UserWidgetResponse) {
    return <UserWidget>{
      id: response.id,
      name: response.widget.name,
      image: response.widget.image,
      type: response.widget.id,
      size: this.getWidgetSize(response.widget.id),
      axisX: response.axis_x,
      axisY: response.axis_y
    };
  }
}
