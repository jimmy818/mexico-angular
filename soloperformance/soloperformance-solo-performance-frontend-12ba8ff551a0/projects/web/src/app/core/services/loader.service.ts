import { Injectable, EventEmitter } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LoaderService {

  status = new EventEmitter<boolean>();

  start(): void {
    this.status.next(true);
  }

  stop(time?:number): void {
    setTimeout(() => {
      this.status.next(false);
    }, time);
  }
}
