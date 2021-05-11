import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'web-upload-image',
  templateUrl: './upload-image.component.html',
  styleUrls: ['./upload-image.component.scss']
})
export class UploadImageComponent implements OnInit {

  @Input() width: number;

  constructor() { }

  ngOnInit(): void {
  }

}
