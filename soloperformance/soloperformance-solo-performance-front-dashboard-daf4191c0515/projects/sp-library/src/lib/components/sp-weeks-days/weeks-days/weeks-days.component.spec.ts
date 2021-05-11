import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WeeksDaysComponent } from './weeks-days.component';

describe('WeeksDaysComponent', () => {
  let component: WeeksDaysComponent;
  let fixture: ComponentFixture<WeeksDaysComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WeeksDaysComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WeeksDaysComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
