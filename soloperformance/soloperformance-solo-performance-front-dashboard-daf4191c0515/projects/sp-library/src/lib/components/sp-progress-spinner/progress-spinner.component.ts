import { Component, Input } from '@angular/core';

@Component({
  selector: 'sp-progress-spinner',
  templateUrl: './progress-spinner.component.html',
  styleUrls: ['./progress-spinner.component.scss']
})
export class ProgressSpinnerComponent {

  /**
   * Obtiene si el control de progreso se está ejecutando.
   */
  @Input() isRunning = false;

  /**
   * Obtiene el texto descriptivo del proceso en ejecución.
   */
  @Input() text: string;

  /**
   * Clases para backdrop de spinner.
   */
  @Input() containerClasses: Array<string> = [];
}
