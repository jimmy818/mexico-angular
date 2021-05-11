import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'web-program',
  templateUrl: './program.component.html',
  styleUrls: ['./program.component.scss']
})
export class ProgramComponent implements OnInit {

  phase: any[] = [
    { name: 'Strenght Upper/Lower', weeks: 5, number: 375 },
    { name: 'Strenght Upper/Lower', weeks: 3, number: 70 },
    { name: 'Strenght Upper/Lower', weeks: 4, number: 234 },
    { name: 'Strenght Upper/Lower', weeks: 5, number: 264 },
  ]
  athletes: any[] = [
    { photo: 'https://randomuser.me/api/portraits/men/3.jpg', name: 'juan' },
    { photo: 'https://randomuser.me/api/portraits/men/89.jpg', name: 'Carlos' },
    { photo: 'https://randomuser.me/api/portraits/men/50.jpg', name: 'Pepe' },
    { photo: 'https://randomuser.me/api/portraits/men/39.jpg', name: 'Cristian' },
    { photo: 'https://randomuser.me/api/portraits/men/43.jpg', name: 'Manuel' },
    { photo: 'https://randomuser.me/api/portraits/men/13.jpg', name: 'Jose' },
  ]
  teams: any[] = [
    { photo: 'https://randomuser.me/api/portraits/men/32.jpg', name: 'juan' },
    { photo: 'https://randomuser.me/api/portraits/men/83.jpg', name: 'Carlos' },
    { photo: 'https://randomuser.me/api/portraits/men/54.jpg', name: 'Pepe' },
    { photo: 'https://randomuser.me/api/portraits/men/36.jpg', name: 'Cristian' },
    { photo: 'https://randomuser.me/api/portraits/men/47.jpg', name: 'Manuel' },
    { photo: 'https://randomuser.me/api/portraits/men/18.jpg', name: 'Jose' },
  ]
  constructor() { }

  ngOnInit(): void {
  }

}
