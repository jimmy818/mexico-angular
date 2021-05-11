import { AfterViewInit, Component, ElementRef, OnInit, QueryList, ViewChild, ViewChildren, ViewEncapsulation } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { of } from 'rxjs';
import { catchError, finalize, map } from 'rxjs/operators';
import { MatIconRegistry } from '@angular/material/icon';
import { GridStack, GridStackNode, GridStackOptions } from 'gridstack';

import { ProgressSpinnerService } from 'sp-core';

import { UserWidget } from '../shared/models/interfaces/user-widget.interface';
import { WidgetService } from '../shared/services/widget.service';
import { Widget } from '../shared/models/interfaces/widget.interface';
import { HeaderGroupAlignment } from 'sp-library';

@Component({
  selector: 'web-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class DashboardComponent implements OnInit, AfterViewInit {

  @ViewChild('gridstack') gridstackRef: ElementRef;
  @ViewChild('container') containerRef: ElementRef;
  @ViewChildren('widget') widgetsRef: QueryList<ElementRef>;

  widgets: Array<UserWidget> = [];

  headerGroupAlignment = HeaderGroupAlignment;

  loadGrid = false;

  private grid: GridStack;

  constructor(
    private iconRegistry: MatIconRegistry,
    private domSanitizer: DomSanitizer,
    private widgetsService: WidgetService,
    private spinnerService: ProgressSpinnerService
  ) {
    this.iconRegistry.addSvgIcon('more_vertical', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/more-vertical.svg'));
  }

  ngOnInit(): void {
    //this.createGrid();
    //this.getWidgets();
  }

  ngAfterViewInit(): void {
    // Por cada cambio que ocurra en el HTML se actualiza el objeto gridstack.
    this.widgetsRef.changes
      .pipe(
        map(() => this.widgetsRef.toArray()),
      )
      .subscribe(gridstackItemsRef => {

        console.log(this.gridstackRef.nativeElement.gridstak);

        // Nuevos widgets
        // const nuevos = this.widgets.filter(widget => widget.id === 0);
        // if (nuevos.length) {
        //   const widgetPosts: Array<Observable<any>> = [];
        //   nuevos.forEach(widget => {
        //     widgetPosts.push(this.widgetsService.addWidgetToUser(widget, 1));
        //   });
        //   this.spinnerService.start();
        //   forkJoin(widgetPosts).pipe(
        //     finalize(() => {
        //       this.spinnerService.stop();
        //     })
        //   ).subscribe(data => {
        //     this.getWidgets();
        //   });

        //   return;
        // }

        //this.createGrid();
        //const last = this.grid.getGridItems()[this.grid.getGridItems().length - 1];
        // last.scrollIntoView({ behavior: "smooth" });
        //this.containerRef.nativeElement.scrollTop = this.gridstackRef.nativeElement.scrollHeight;
        //console.log('agregado')

        // this.grid.removeAll();
        // gridstackItemsRef.forEach(gi => {
        //   this.grid.addWidget(gi.nativeElement, { width: +gi.nativeElement.dataset.gsWidth, height: +gi.nativeElement.dataset.gsHeight })
        // })







      });
  }

  getWidgets(): void {
    this.spinnerService.start();
    this.widgetsService
      .getUserWidgets()
      .pipe(
        catchError(error => {
          return of<Array<UserWidget>>([]);
        }),
        finalize(() => {
          this.spinnerService.stop();
        })
      )
      .subscribe(widgets => {
        this.widgets = widgets;

        //   this.widgets.forEach(widget => {
        //     this.grid.addWidget(`<sp-card class="grid-stack-item-header">
        //     <sp-header class="mt-n3" [fluid]="true">
        //         <sp-header-group [expanded]="true" [isTitle]="true">
        //             {{widget.name}}
        //         </sp-header-group>
        //         <sp-header-group [alignment]="headerGroupAlignment.right">
        //             <button mat-icon-button [matMenuTriggerFor]="menu">
        //                 <mat-icon svgIcon="more_vertical"></mat-icon>
        //             </button>
        //             <mat-menu #menu="matMenu" xPosition="before">
        //                 <button mat-menu-item (click)="deleteWidget(widget)">Erase widget</button>
        //                 <button mat-menu-item (click)="duplicateWidget(widget)">Duplicate widget</button>
        //             </mat-menu>
        //         </sp-header-group>
        //     </sp-header>
        //     <div class="dashboard__widget-container">
        //         <span>{{widget.name}}</span>
        //     </div>
        // </sp-card>`, { width: widget.size, height: 4 })

        // });
      })
  }

  onWidgetPreviewClick(widget: Widget): void {
    //this.addWidget(widget);
  }

  /**
   * Crea o inicializa el objeto gridstack para grid dinámicos.
   */
  private createGrid() {

    // Destruye el grid para reconstruir en base a los elementos widgets creados.
    if (this.grid) {
      this.grid.destroy(false);
    }

    this.grid = GridStack.init(<GridStackOptions>{
      alwaysShowResizeHandle: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
        navigator.userAgent
      ),
      disableResize: true,
      oneColumnModeDomSort: true
    });


    this.grid.on('change', (e, items: GridStackNode[]) => {
      // var str = '';
      // items.forEach(function (item) { str += ' (x,y)=' + item.x + ',' + item.y; });
      // console.log(e.type + ' ' + items.length + ' items:' + str);
      items.forEach(() => {
        console.log('modificado')
      })
    })
  }

  deleteWidget(userWidget: UserWidget): void {
    this.spinnerService.start();
    this.widgetsService
      .removeWidgetFromUser(userWidget.id)
      .pipe(
        finalize(() => {
          this.spinnerService.stop();
        })
      ).subscribe(response => {
        this.getWidgets();
      });
  }
}
