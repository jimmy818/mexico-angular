import { Component, Input, OnInit } from '@angular/core';

import { HeaderGroupAlignment } from 'sp-library';

import { Widget } from '../shared/models/interfaces/widget.interface';
import { GridStackItemContent } from '../shared/models/interfaces/grid-stack-item-content.interface';
import { WidgetService } from '../shared/services/widget.service';

@Component({
  selector: 'web-widget-teams-calendar',
  templateUrl: './widget-teams-calendar.component.html',
  styleUrls: ['./widget-teams-calendar.component.scss']
})
export class WidgetTeamsCalendarComponent implements GridStackItemContent, OnInit {

  @Input() widget: Widget;

  headerGroupAlignment = HeaderGroupAlignment;

  constructor(
    private widgetService: WidgetService
  ) { }

  ngOnInit(): void {
  }

  deleteWidget(): void {
    this.widgetService.requestRemoveWidgetFromUser(this.widget.gridStackItemId);
  }

  duplicateWidget(): void {
    this.widgetService.requestDuplicateWidgetFromUser(this.widget);
  }
}
