import { Component, ElementRef, OnInit, OnDestroy, Renderer2, ViewChild } from '@angular/core';
import { Subscription } from 'rxjs';

import { ProgressSpinnerService } from 'sp-core';

@Component({
  selector: 'web-main-layout',
  templateUrl: './main-layout.component.html',
  styleUrls: ['./main-layout.component.scss']
})
export class MainLayoutComponent implements OnInit, OnDestroy {

  spinnerIsRunning = false;

  @ViewChild('header', { read: ElementRef }) headerRef: ElementRef;

  private spinnerStateSubscription: Subscription;

  constructor(
    private renderer: Renderer2,
    private spinnerService: ProgressSpinnerService
  ) {
    this.spinnerService.delay = 500;
  }

  ngOnInit(): void {
    this.spinnerStateSubscription = this.spinnerService
      .stateChange
      .subscribe(state => this.spinnerIsRunning = state);
  }

  ngOnDestroy(): void {
    if (this.spinnerStateSubscription) {
      this.spinnerStateSubscription.unsubscribe();
    }
  }

  ngAfterViewInit(): void {

    // Visualiza una sombra en la parte inferior del encabezado. Cuando el contenido del cuerpo alcanza el límite inferior del encabezado.
    // Actualmente se está manejando un margen de 1.5rem
    const bodyMarginTop = parseFloat(getComputedStyle(document.documentElement).fontSize) * 1.5;
    let header = this.headerRef.nativeElement;
    window.onscroll = (() => {
      if (window.pageYOffset >= bodyMarginTop) {
        this.renderer.addClass(header, 'sp-header--raised');
      } else {
        this.renderer.removeClass(header, 'sp-header--raised');
      }
    });
  }

}
