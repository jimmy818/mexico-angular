import { TestBed } from '@angular/core/testing';

import { InstitutionManagerService } from './institution-manager.service';

describe('InstitutionManagerService', () => {
  let service: InstitutionManagerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InstitutionManagerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
