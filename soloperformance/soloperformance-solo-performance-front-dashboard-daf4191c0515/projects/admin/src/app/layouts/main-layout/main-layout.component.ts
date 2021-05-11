import { Component, ElementRef, OnInit, Renderer2, ViewChild } from '@angular/core';

@Component({
  selector: 'admin-main-layout',
  templateUrl: './main-layout.component.html',
  styleUrls: ['./main-layout.component.scss']
})
export class MainLayoutComponent implements OnInit {

  @ViewChild('header', { read: ElementRef }) headerRef: ElementRef;

  constructor(
    private renderer: Renderer2
  ) { }

  ngOnInit(): void {
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
