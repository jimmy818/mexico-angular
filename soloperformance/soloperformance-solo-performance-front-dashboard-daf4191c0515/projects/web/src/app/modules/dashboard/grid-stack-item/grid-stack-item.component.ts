import { Component, ComponentFactoryResolver, Input, OnInit, ViewChild } from '@angular/core';
import { GridStackItemContent } from '../shared/models/interfaces/grid-stack-item-content.interface';
import { GridStackItem } from '../shared/models/interfaces/grid-stack-item.interface';
import { ViewContainerDirective } from 'sp-library';

@Component({
  selector: 'web-grid-stack-item',
  templateUrl: './grid-stack-item.component.html',
  styleUrls: ['./grid-stack-item.component.scss']
})
export class GridStackItemComponent implements OnInit {

  @Input() gridStackItem: GridStackItem;

  @ViewChild(ViewContainerDirective, { static: true }) webGridStackItem: ViewContainerDirective;

  constructor(private componentFactoryResolver: ComponentFactoryResolver) { }

  ngOnInit(): void {

    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.gridStackItem.content);

    const viewContainerRef = this.webGridStackItem.viewContainerRef
    viewContainerRef.clear();

    const componentRef = viewContainerRef.createComponent<GridStackItemContent>(componentFactory);
    componentRef.instance.widget = this.gridStackItem.widget;
  }
}
