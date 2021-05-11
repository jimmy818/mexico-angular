import { NgModule } from '@angular/core';

import { DragScrollModule } from 'ngx-drag-scroll';

import { SharedModule } from '@web/shared/shared.module';
import { CalendarItemModule } from '@web/shared/components/calendar-item/calendar-item.module';
import { EventsModule } from '@web/shared/components/events/events.module';
import { DashboardRoutingModule } from './dashboard-routing.module';

import { DashboardComponent } from './dashboard/dashboard.component';
import { GridStackItemComponent } from './grid-stack-item/grid-stack-item.component';
import { GridStackComponent } from './grid-stack/grid-stack.component';
import { StatsChartComponent } from './stats-chart/stats-chart.component';
import { MainWidgetComponent } from './main-widget/main-widget.component';
import { WidgetPreviewComponent } from './widget-preview/widget-preview.component';
import { WidgetSidebarComponent } from './widget-sidebar/widget-sidebar.component';
import { WidgetTeamsCalendarComponent } from './widget-teams-calendar/widget-teams-calendar.component';

const COMPONENTS = [
  DashboardComponent,
  WidgetSidebarComponent,
  WidgetPreviewComponent,
  MainWidgetComponent,
  WidgetTeamsCalendarComponent,
  GridStackComponent,
  GridStackItemComponent,
  StatsChartComponent
]

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    DragScrollModule,
    DashboardRoutingModule,
    CalendarItemModule,
    EventsModule,
    SharedModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class DashboardModule { }
