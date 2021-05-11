import { Component, ComponentFactoryResolver, ComponentRef, DoCheck, Injector, OnDestroy, OnInit, ViewEncapsulation } from '@angular/core';
import { of, forkJoin, Observable } from 'rxjs';
import { catchError, finalize } from 'rxjs/operators';
import { SubSink } from 'subsink';
import { GridStack, GridStackOptions, GridStackNode } from 'gridstack';

import { ProgressSpinnerService } from 'sp-core';

import { GridStackItem } from '../shared/models/interfaces/grid-stack-item.interface';
import { Widget } from '../shared/models/interfaces/widget.interface';
import { WidgetService } from '../shared/services/widget.service';
import { UserWidget } from '../shared/models/interfaces/user-widget.interface';
import { GridStackMetadata } from '../shared/models/interfaces/grid-stack-metadata.interface';
import { WidgetType } from '../shared/models/enums/widget-type.enum';

import { GridStackItemComponent } from '../grid-stack-item/grid-stack-item.component';
import { MainWidgetComponent } from '../main-widget/main-widget.component';
import { WidgetTeamsCalendarComponent } from '../widget-teams-calendar/widget-teams-calendar.component';

@Component({
  selector: 'web-grid-stack',
  templateUrl: './grid-stack.component.html',
  styleUrls: ['./grid-stack.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class GridStackComponent implements OnInit, OnDestroy, DoCheck {

  userWidgets: Array<UserWidget> = [];

  private grid: GridStack;

  private subsink = new SubSink();

  private gridStackMetadata: Array<GridStackMetadata> = [];

  constructor(
    private resolver: ComponentFactoryResolver,
    private injector: Injector,
    private widgetService: WidgetService,
    private spinnerService: ProgressSpinnerService
  ) { }

  ngOnInit(): void {

    // Observa cada que se solicita agregar un nuevo widget al usuario
    this.subsink.sink = this.widgetService.widgetAddRequested$
      .subscribe(widget => {
        this.addWidget(widget);
      });

    // Observa cada que se solicita duplicar un widget y asignar al usuario
    this.subsink.sink = this.widgetService.widgetDuplicateRequested$
      .subscribe(widget => {
        this.addWidget(widget);
      })

    // Observa cada que se solicita eliminar un widget al usuario
    this.subsink.sink = this.widgetService.userWidgetRemoveRequested$
      .subscribe(widgetId => {
        this.removeWidget(widgetId);
      });

    // Inicializa el grid
    this.grid = GridStack.init(<GridStackOptions>{
      // alwaysShowResizeHandle: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      //   navigator.userAgent
      // )
      disableResize: true,
      cellHeight: 100
    });

    // Escucha el evento de agregar nuevo widget.
    this.grid.on('added', (event: Event, items: Array<GridStackNode>) => {
      items.forEach(item => {
        // Agrega o asigna el widget al usuario en sesión.
        const widgetMetadata = this.findWidgetMetadata(+item.id);
        // Sólo se agrega en caso de que no tenga ya la asignación (userWidget). Si tiene asignación significa que es un registro obtenido de BD.
        if (widgetMetadata && !widgetMetadata.userWidget) {
          this.spinnerService.start();
          this.widgetService
            .addWidgetToUser(widgetMetadata.widget, item.x, item.y)
            .pipe(
              catchError(error => {
                return of(<UserWidget>{});
              }),
              finalize(() => {
                this.spinnerService.stop();
              })
            )
            .subscribe(response => {
              widgetMetadata.userWidget = response;
            });
        }
      });
    });

    // Escucha el evento de modificar propiedades de widgets. Para verificar cambio de posición.
    this.grid.on('change', (event: Event, items: Array<GridStackNode>) => {

      // Acumula en un arreglo las actualizaciones a realizar en bd por cada item modificado.
      // Para que asimile un sólo proceso (Sólo una vez se visualiza y oculta spinner).
      const updates: Array<Observable<boolean>> = [];
      items.forEach(item => {
        const widgetMetadata = this.findWidgetMetadata(+item.id);
        if (widgetMetadata && widgetMetadata.userWidget) {
          widgetMetadata.userWidget.axisX = item.x;
          widgetMetadata.userWidget.axisY = item.y;
          updates.push(this.widgetService.updateWidgetUser(widgetMetadata.userWidget));
        }
      });
      // Envía a actualizar en BD todos los items modificados.
      this.spinnerService.start();
      forkJoin(updates)
        .pipe(
          catchError(error => {
            return of(false);
          }),
          finalize(() => {
            this.spinnerService.stop();
          })
        )
        .subscribe(() => { });
    });

    // Escucha el evento de eliminar un widget.
    this.grid.on('removed', (event: Event, items: Array<GridStackNode>) => {
      items.forEach(item => {
        // Elimina la asignación del widget al usuario en sesión.
        const widgetMetadata = this.findWidgetMetadata(+item.id);
        if (widgetMetadata && widgetMetadata.userWidget) {
          this.spinnerService.start();
          this.widgetService
            .removeWidgetFromUser(widgetMetadata.userWidget.id)
            .pipe(
              catchError(error => {
                return of(false);
              }),
              finalize(() => {
                this.spinnerService.stop();
              })
            )
            .subscribe(() => { });
        }
      });
    });

    // Obtiene los widgets del usuario.
    this.spinnerService.start();
    this.widgetService
      .getUserWidgets()
      .pipe(
        catchError(() => {
          return of(<Array<UserWidget>>[])
        }),
        finalize(() => {
          this.spinnerService.stop();
        })
      )
      .subscribe(response => {
        this.userWidgets = response;
        this.userWidgets.forEach(userWidget => {
          this.addWidget(
            <Widget>{
              type: userWidget.type,
              name: userWidget.name,
              image: userWidget.image,
              size: this.widgetService.getWidgetSize(userWidget.type)
            },
            userWidget
          );
        })
      });
  }

  ngOnDestroy() {
    this.subsink.unsubscribe();
    this.gridStackMetadata.forEach(item => {
      item.component.destroy();
    })
  }

  ngDoCheck(): void {
    this.gridStackMetadata.forEach(item => {
      item.component.changeDetectorRef.detectChanges();
    })
  }

  private addWidget(
    widget: Widget,
    userWidget: UserWidget = null
  ) {

    const widgetToadd: Widget = JSON.parse(JSON.stringify(widget));
    const id = this.gridStackMetadata.length + 1;

    // Construye dinámicamente el componente item. Dedido a que requiere renderizar el html como parte angular.
    const component = this.createDynamicItem(widgetToadd, id);

    // Elemento HTML nativo del componente, es la que finalmente se agregará en el grid.
    const htmlElement = <HTMLElement>component.location.nativeElement;

    // Se almacena en una colección para referencias posterior.
    this.gridStackMetadata.push({
      id: id,
      gridStackItem: htmlElement,
      component: component,
      widget: widgetToadd,
      userWidget: userWidget  /* En caso de que no se envíe significa que se está agregando recién y no se obtuvo de BD */
    });

    // Altura de widget.
    let widgetHeight = 0;
    switch (widgetToadd.type) {
      case WidgetType.mainWidget:
        widgetHeight = 9;
        break;
      default:
        widgetHeight = 4;
        break;
    }

    // Agrega un nuevo widget al grid.
    this.grid.addWidget(htmlElement, {
      id: id,
      width: widgetToadd.size,
      height: widgetHeight,
      x: userWidget ? userWidget.axisX : null,
      y: userWidget ? userWidget.axisY : null
    });

    // Visualiza o enfoca el elemento recién agregado.
    // Siempre y cuando no sea un registro obtenido de BD.
    if (!userWidget) {
      setTimeout(() => {
        htmlElement.scrollIntoView({ behavior: "smooth" });
      }, 0);
    }
  }

  /**
   * Elimina un widget del grid
   * @param gridStackItemId Identificador de widget a eliminar
   */
  private removeWidget(gridStackItemId: number) {
    const item = this.findWidgetMetadata(gridStackItemId);
    if (item) {
      // Elimina el widget del grid.
      this.grid.removeWidget(item.gridStackItem);
      // Elimina el componente angular que corresponde al widget.
      item.component.destroy();
      // Elimina el registro de la colección de items.
      const itemIndex = this.gridStackMetadata.indexOf(item);
      this.gridStackMetadata.splice(itemIndex, 1);
    }
  }

  /**
   * Construye dinámicamente el componente item. Dedido a que requiere renderizar el html como parte angular.
   * @param widget Datos de widget
   */
  private createDynamicItem(
    widget: Widget,
    widgetId: number
  ): ComponentRef<GridStackItemComponent> {

    const factory = this.resolver.resolveComponentFactory(GridStackItemComponent);
    const component = factory.create(this.injector);

    const data = new GridStackItem();
    switch (widget.type) {
      case WidgetType.mainWidget:
        data.content = MainWidgetComponent;
        break;
      default:
        data.content = WidgetTeamsCalendarComponent
        break;
    }

    data.widget = widget;
    data.widget.gridStackItemId = widgetId;
    component.instance.gridStackItem = data;
    component.changeDetectorRef.detectChanges();

    return component;
  }

  private findWidgetMetadata(
    gridStackItemId: number
  ): GridStackMetadata {

    const items = this.gridStackMetadata.filter(item => item.id === gridStackItemId);
    if (!items.length) {
      return null;
    }

    return items[0];
  }
}
