import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HeaderGroupComponent } from './header-group.component';

describe('HeaderGroupComponent', () => {
  let component: HeaderGroupComponent;
  let fixture: ComponentFixture<HeaderGroupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HeaderGroupComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HeaderGroupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
