import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';

@Component({
  selector: 'sp-dialog-content',
  templateUrl: './dialog-content.component.html',
  styleUrls: ['./dialog-content.component.scss']
})
export class DialogContentComponent implements OnInit {

  @ViewChild(TemplateRef) contentContent: TemplateRef<any>;
  
  constructor() { }

  ngOnInit(): void {
  }

}
