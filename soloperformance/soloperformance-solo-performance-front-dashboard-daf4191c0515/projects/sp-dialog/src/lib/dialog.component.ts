import { AfterContentInit, Component, ContentChild, Input, OnInit } from '@angular/core';

import { DialogActionsComponent } from './dialog-actions/dialog-actions.component';
import { DialogContentComponent } from './dialog-content/dialog-content.component';
import { DialogTitleComponent } from './dialog-title/dialog-title.component';

@Component({
  selector: 'sp-dialog',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.scss']
})
export class DialogComponent implements OnInit, AfterContentInit {

  @Input() isCloseButtonVisible = false;

  @Input() dialogContentClass = '';

  @ContentChild(DialogTitleComponent) titleComponent: DialogTitleComponent;
  @ContentChild(DialogContentComponent) contentComponent: DialogContentComponent;
  @ContentChild(DialogActionsComponent) actionsComponent: DialogActionsComponent;

  title: DialogTitleComponent;
  content: DialogContentComponent;
  actions: DialogActionsComponent;

  constructor() { }

  ngOnInit(): void {
  }

  ngAfterContentInit() {
    setTimeout(() => {
      this.title = this.titleComponent;
      this.content = this.contentComponent;
      this.actions = this.actionsComponent;
    }, 0);
  }
}
