import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WidgetTeamsCalendarComponent } from './widget-teams-calendar.component';

describe('WidgetTeamsCalendarComponent', () => {
  let component: WidgetTeamsCalendarComponent;
  let fixture: ComponentFixture<WidgetTeamsCalendarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WidgetTeamsCalendarComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WidgetTeamsCalendarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
