import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[spViewContainer]'
})
export class ViewContainerDirective {

  constructor(public viewContainerRef: ViewContainerRef) { }

}
