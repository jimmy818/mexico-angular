import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'web-widget-preview',
  templateUrl: './widget-preview.component.html',
  styleUrls: ['./widget-preview.component.scss']
})
export class WidgetPreviewComponent implements OnInit {

  @Input() name: string;
  @Input() image: string;

  constructor() { }

  ngOnInit(): void {
  }

}
