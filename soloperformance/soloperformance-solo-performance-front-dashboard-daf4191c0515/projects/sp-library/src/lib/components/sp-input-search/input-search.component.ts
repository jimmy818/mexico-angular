import { Component, ElementRef, EventEmitter, Input, OnInit, Output, Renderer2, ViewChild, ViewEncapsulation, OnChanges, SimpleChanges } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';

@Component({
  selector: 'sp-input-search',
  templateUrl: './input-search.component.html',
  styleUrls: ['./input-search.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class InputSearchComponent {

  @Input() placeholder = 'Search';

  /**
   * Obtiene o establece si el control creará los parámetros en URL.
   */
  @Input() createParams = true;

  /**
   * Obtiene o el width.
   */
  @Input() width: number;

  @Input() search: string;

  @Input() disableAnimation = false;

  @Output() valueChange = new EventEmitter<string>();

  @Output() focus = new EventEmitter<null>();

  @Output() blur = new EventEmitter<null>();

  @Output() enter = new EventEmitter<string>();

  @ViewChild('container') containerRef: ElementRef;

  @ViewChild('input') inputRef: ElementRef;

  get container(): HTMLElement {
    return <HTMLElement>this.containerRef.nativeElement;
  }

  get input(): HTMLInputElement {
    return <HTMLInputElement>this.inputRef.nativeElement;
  }

  constructor(
    private iconRegistry: MatIconRegistry,
    private domSanitizer: DomSanitizer,
    private renderer: Renderer2,
    private r: Router
  ) {
    this.iconRegistry.addSvgIcon('search', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/search.svg'));
    this.iconRegistry.addSvgIcon('close', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/close.svg'));
  }

  onFocus(): void {
    this.renderer.addClass(this.container, 'sp-input-search__container--focus');
    this.focus.emit();
  }

  onBlur(): void {
    this.renderer.removeClass(this.container, 'sp-input-search__container--focus');
    this.blur.emit();
  }

  onSearchChange(): void {
    this.valueChange.emit(this.search);
    if (this.createParams) {
      const wordSearch = this.search;
      setTimeout(() => {
        if (wordSearch == this.search) {
          this.search = this.search != '' ? this.search : null;
          const urlTree = this.r.createUrlTree([], {
            queryParams: { search: this.search },
            queryParamsHandling: "merge",
            preserveFragment: true
          });
          this.r.navigateByUrl(urlTree);
        }
      }, 750);
    }
  }

  onKeyEnter(text: string): void {
    this.enter.emit(text);
  }
}
