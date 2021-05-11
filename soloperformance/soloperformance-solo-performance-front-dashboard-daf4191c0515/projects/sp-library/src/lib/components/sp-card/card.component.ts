import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'sp-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.scss']
})
export class CardComponent implements OnInit {

  /**
   * Obtiene o establece si la tarjeta se expandirá hasta ocupar el 100% de su altura.
   */
  @Input() expand = false;
  @Input() class: string;

  constructor() { }

  ngOnInit(): void { }

}
