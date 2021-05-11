import { Directive, HostListener } from '@angular/core';

@Directive({
  selector: '[spClickStopPropagation]'
})
export class ClickStopPropagationDirective {

  @HostListener('click', ['$event'])
  public click(event: any): void {
    event.stopPropagation();
  }
}
