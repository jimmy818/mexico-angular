import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkoutWeeksDaysComponent } from './workout-weeks-days.component';

describe('WorkoutWeeksDaysComponent', () => {
  let component: WorkoutWeeksDaysComponent;
  let fixture: ComponentFixture<WorkoutWeeksDaysComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WorkoutWeeksDaysComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WorkoutWeeksDaysComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
