import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfilingComponent } from './profiling.component';

describe('LibraryComponent', () => {
  let component: ProfilingComponent;
  let fixture: ComponentFixture<ProfilingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfilingComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfilingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
