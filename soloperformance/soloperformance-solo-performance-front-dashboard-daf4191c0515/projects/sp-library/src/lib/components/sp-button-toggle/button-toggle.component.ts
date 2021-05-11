import { Component, OnInit, Input, ViewEncapsulation, Output, EventEmitter } from '@angular/core';
import { MatButtonToggleChange } from '@angular/material/button-toggle';

@Component({
  selector: 'sp-button-toggle',
  templateUrl: './button-toggle.component.html',
  styleUrls: ['./button-toggle.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class ButtonToggleComponent implements OnInit {

  @Input() changeText = '';
  @Input() checked = false;
  @Input() disabled = false;
  @Input() color = '#ffffff';

  @Output() change = new EventEmitter<boolean>();

  constructor() { }

  ngOnInit(): void { }

  onMatButtonToggleChange(change: MatButtonToggleChange): void {
    this.change.emit(change.source.checked);
  }
}
