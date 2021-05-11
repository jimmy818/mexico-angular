import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'web-imgs',
  templateUrl: './imgs.component.html',
  styleUrls: ['./imgs.component.scss']
})
export class ImgsComponent implements OnInit {

  @Input() imgs: Array<any> = [];
  @Input() max: number;
  @Input() color: string;
  @Input() key: string = 'photo';

  constructor() { }

  ngOnInit(): void {
  }

}
