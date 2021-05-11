import { Component, Input, OnInit, TemplateRef, ViewChild } from '@angular/core';

@Component({
  selector: 'sp-dialog-title',
  templateUrl: './dialog-title.component.html',
  styleUrls: ['./dialog-title.component.scss']
})
export class DialogTitleComponent implements OnInit {

  @Input() title: string;
  @Input() subtitle: string;

  @ViewChild(TemplateRef) titleContent: TemplateRef<any>;

  constructor() { }

  ngOnInit(): void {
  }

}
