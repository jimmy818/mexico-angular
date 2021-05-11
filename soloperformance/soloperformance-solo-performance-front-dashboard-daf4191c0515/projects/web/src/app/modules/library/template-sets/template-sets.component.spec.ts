import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TemplateSetsComponent } from './template-sets.component';

describe('TemplateSetsComponent', () => {
  let component: TemplateSetsComponent;
  let fixture: ComponentFixture<TemplateSetsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TemplateSetsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TemplateSetsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
