import { Component, ElementRef, EventEmitter, HostListener, OnDestroy, OnInit, Output, Renderer2, ViewChild } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Subject, Subscription, throwError } from 'rxjs';
import { catchError, finalize } from 'rxjs/operators';

import { ProgressSpinnerService, RequestParam, REQUEST_PARAM_NAMES } from 'sp-core';

import { Widget } from '../shared/models/interfaces/widget.interface';
import { WidgetService } from '../shared/services/widget.service';

@Component({
  selector: 'web-widget-sidebar',
  templateUrl: './widget-sidebar.component.html',
  styleUrls: ['./widget-sidebar.component.scss']
})
export class WidgetSidebarComponent implements OnInit, OnDestroy {

  @ViewChild('sidebar') sidebarRef: ElementRef;
  @ViewChild('sidebarContainer') sidebarContainerRef: ElementRef;
  @ViewChild('floatingButton') floatingButtonRef: ElementRef;

  @Output() widgetPreviewClick = new EventEmitter<Widget>();

  @HostListener('window:keydown', ['$event'])
  handleKeyDown(event: KeyboardEvent) {
    if (event.key != undefined && event.key.toLowerCase() === "escape") {
      this.sidebarIsOpen = true;
      this.showHideWidgets();
    }
    else if (event.keyCode != undefined && event.keyCode === 27) {
      this.sidebarIsOpen = true;
      this.showHideWidgets();
    }
  }

  /**
   * Evento click del documento para determinar si se oculta el dropdown de elementos.
   * @param event Evento click del mouse
   */
  @HostListener('document:click', ['$event'])
  documentClick(event: MouseEvent): void {
    if (!event.target) {
      return;
    }
    // Verifica si el elemento donde se realizó el evento está contenido en el elemento HOST de la directiva.
    let contains = this.sidebarContainerRef.nativeElement.contains(event.target);
    if (!contains) {
      this.sidebarIsOpen = true;
      this.showHideWidgets();
    }
  }

  widgets: Array<Widget> = [];

  isLoading = false;

  sidebarIsOpen = false;

  private search: string;

  private spinnerSubject = new Subject<boolean>();
  private spinnerSubscription: Subscription;

  private searchTimeout: any;

  private get sidebar(): HTMLElement {
    return this.sidebarRef.nativeElement;
  }

  private get floatingButton(): HTMLElement {
    return this.floatingButtonRef.nativeElement;
  }

  constructor(
    private iconRegistry: MatIconRegistry,
    private domSanitizer: DomSanitizer,
    private renderer: Renderer2,
    private widgetService: WidgetService,
    private spinnerService: ProgressSpinnerService
  ) {
    this.iconRegistry.addSvgIcon('close', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/close.svg'));
    this.iconRegistry.addSvgIcon('widget', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/widget.svg'));
  }

  ngOnInit(): void {

    // Se queda escuchando cada cambio de estatus del spinner.
    this.spinnerSubscription = this.spinnerService
      .isLoadingSubject(this.spinnerSubject)
      .subscribe(isLoading => this.isLoading = isLoading);

    this.getWidgets();
  }

  ngOnDestroy(): void {
    if (this.spinnerSubscription) {
      this.spinnerSubscription.unsubscribe();
    }
  }

  showHideWidgets(): void {
    if (this.sidebarIsOpen) {
      this.renderer.removeClass(this.sidebar, 'sp-widget-sidebar--open');
      this.renderer.removeClass(this.floatingButton, 'sp-widget-sidebar__floating-btn--hidden');
    } else {
      this.renderer.addClass(this.sidebar, 'sp-widget-sidebar--open');
      this.renderer.addClass(this.floatingButton, 'sp-widget-sidebar__floating-btn--hidden');
    }
    this.sidebarIsOpen = !this.sidebarIsOpen;
  }

  onSearchEnter(text: string): void {
    // this.search = text ? text : null;
    // this.getWidgets();
  }

  onSearchValueChange(text: string): void {
    if (this.searchTimeout) {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = null;
    }
    this.searchTimeout = setTimeout(() => {
      this.search = text;
      this.getWidgets()
    }, 500);
  }

  onWidgetDrop(e: any): void {
    console.log(e)
  }

  onWidgetPreviewClick(widget: Widget): void {
    this.widgetService.requestAddWidgetToUser(widget);
  }

  private getWidgets(): void {

    const params: Array<RequestParam> = [];
    if (this.search) {
      params.push({
        key: REQUEST_PARAM_NAMES.search,
        value: this.search
      })
    }

    this.spinnerSubject.next(true);
    this.widgetService
      .getWidgets(params)
      .pipe(
        catchError((error) => {
          this.spinnerSubject.next(false);
          return throwError(error);
        }),
        finalize(() => {
          this.spinnerSubject.next(false);
        })
      )
      .subscribe(data => {
        this.widgets = data;
      });
  }
}
