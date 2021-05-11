import { AfterContentInit, Component, ContentChild, ContentChildren, Input, OnInit, QueryList } from '@angular/core';
import { Observable } from 'rxjs';
import { startWith, map, delay } from "rxjs/operators";

import { HeaderGroupAlignment } from './header-group/enums/header-group-alignment.enum';

import { HeaderGroupComponent } from './header-group/header-group.component';
import { HeaderIconComponent } from './header-icon/header-icon.component';

@Component({
  selector: 'sp-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit, AfterContentInit {

  /**
   * Elimina márgenes, paddings.
   */
  @Input() fluid = false;

  @ContentChild(HeaderIconComponent) logo: HeaderIconComponent;
  @ContentChildren(HeaderGroupComponent) groups: QueryList<HeaderGroupComponent>;

  groupItems: Observable<Array<HeaderGroupComponent>>;

  groupAlignment = HeaderGroupAlignment;

  constructor() { }

  ngOnInit(): void {
  }

  ngAfterContentInit(): void {
    this.groupItems = this.groups.changes
      .pipe(startWith(''))
      .pipe(delay(0))
      .pipe(map(() => this.groups.toArray()));
  }
}
