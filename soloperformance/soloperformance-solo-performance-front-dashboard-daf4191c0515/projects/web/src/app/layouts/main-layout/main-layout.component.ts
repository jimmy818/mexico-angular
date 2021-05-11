import { Component, ElementRef, OnInit, OnDestroy, Renderer2, ViewChild } from '@angular/core';
import { SubSink } from 'subsink';

import { ProgressSpinnerService } from 'sp-core';

@Component({
  selector: 'web-main-layout',
  templateUrl: './main-layout.component.html',
  styleUrls: ['./main-layout.component.scss']
})
export class MainLayoutComponent implements OnInit, OnDestroy {

  spinnerIsRunning = false;

  @ViewChild('header', { read: ElementRef }) headerRef: ElementRef;
  @ViewChild('main') mainRef: ElementRef;

  private subsink = new SubSink();

  get header(): HTMLElement {
    return this.headerRef.nativeElement;
  }

  get main(): HTMLElement {
    return this.mainRef.nativeElement;
  }

  constructor(
    private renderer: Renderer2,
    private spinnerService: ProgressSpinnerService
  ) {
    this.spinnerService.delay = 500;
  }

  ngOnInit(): void {
    this.subsink.sink = this.spinnerService
      .stateChange
      .subscribe(state => this.spinnerIsRunning = state);
  }

  ngOnDestroy(): void {
    this.subsink.unsubscribe();
  }

  ngAfterViewInit(): void {

    // Visualiza una sombra en la parte inferior del encabezado. Cuando el contenido del cuerpo alcanza el límite inferior del encabezado.
    // Actualmente se está manejando un margen de 1.5rem
    const bodyMarginTop = parseFloat(getComputedStyle(document.documentElement).fontSize) * 1.5;
    this.main.onscroll = () => {
      if (this.main.scrollTop >= bodyMarginTop) {
        this.renderer.addClass(this.header, 'sp-header--raised');
      } else {
        this.renderer.removeClass(this.header, 'sp-header--raised');
      }
    }
  }

}
