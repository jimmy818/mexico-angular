import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';

@Component({
  selector: 'sp-dialog-actions',
  templateUrl: './dialog-actions.component.html',
  styleUrls: ['./dialog-actions.component.scss']
})
export class DialogActionsComponent implements OnInit {

  @ViewChild(TemplateRef) actionsContent: TemplateRef<any>;

  constructor() { }

  ngOnInit(): void {
  }

}
