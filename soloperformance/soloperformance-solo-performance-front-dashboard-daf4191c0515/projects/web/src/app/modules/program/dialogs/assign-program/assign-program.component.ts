import { Component, OnInit, ViewChild } from '@angular/core';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { MatSelectionList } from '@angular/material/list';
import { ApiService } from '@web/core/services/api.service';

interface Team {
  id: number;
  name: string;
  photo: string;
}
interface Athlete {
  id: number;
  name: string;
  photo: string;
  selected: boolean;
}

@Component({
  selector: 'web-assign-program',
  templateUrl: './assign-program.component.html',
  styleUrls: ['./assign-program.component.scss']
})
export class AssignProgramComponent implements OnInit {

  @ViewChild('athletesList') athletesList: MatSelectionList;

  teams: Team[] = [];
  team: Team;
  athletes: Array<Athlete> = [];
  selectAllAthletesChecked = false;

  constructor(
    private API: ApiService
  ) {
    this.API.get(`team-profile/?institution=47`).subscribe((data: any) => { })

    this.teams = [
      { id: 2, name: "Arizona Diamondbacks", photo: "https://media.api-sports.io/baseball/teams/2.png", },
      { id: 3, name: "Atlanta Braves", photo: "https://media.api-sports.io/baseball/teams/3.png", },
      { id: 4, name: "Baltimore Orioles", photo: "https://media.api-sports.io/baseball/teams/4.png", },
      { id: 5, name: "Boston Red Sox", photo: "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/bos.png&h=80&w=80&scale=crop&cquality=40&location=origin", },
      { id: 6, name: "Chicago Cubs", photo: "https://media.api-sports.io/baseball/teams/6.png", },
      { id: 7, name: "Chicago White Sox", photo: "https://media.api-sports.io/baseball/teams/7.png", },
      { id: 8, name: "Cincinnati Reds", photo: "https://media.api-sports.io/baseball/teams/8.png", },
      { id: 9, name: "Cleveland Indians", photo: "https://media.api-sports.io/baseball/teams/9.png", },
      { id: 10, name: "Colorado Rockies", photo: "https://media.api-sports.io/baseball/teams/10.png", },
      { id: 12, name: "Detroit Tigers", photo: "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/det.png&h=80&w=80&scale=crop&cquality=40&location=origin", },
      { id: 15, name: "Houston Astros", photo: "https://media.api-sports.io/baseball/teams/15.png", },
      { id: 16, name: "Kansas City Royals", photo: "https://media.api-sports.io/baseball/teams/16.png", },
      { id: 17, name: "Los Angeles Angels", photo: "https://media.api-sports.io/baseball/teams/17.png", },
      { id: 18, name: "Los Angeles Dodgers", photo: "https://media.api-sports.io/baseball/teams/18.png", },
      { id: 19, name: "Miami Marlins", photo: "https://media.api-sports.io/baseball/teams/19.png", },
      { id: 20, name: "Milwaukee Brewers", photo: "https://media.api-sports.io/baseball/teams/20.png", },
      { id: 22, name: "Minnesota Twins", photo: "https://media.api-sports.io/baseball/teams/22.png", },
      { id: 23, name: "National League", photo: "https://media.api-sports.io/baseball/teams/23.png", },
      { id: 24, name: "New York Mets", photo: "https://media.api-sports.io/baseball/teams/24.png", },
      { id: 25, name: "New York Yankees", photo: "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/nyy.png&h=80&w=80&scale=crop&cquality=40&location=origin", },
      { id: 43, name: "Northeastern", photo: "https://media.api-sports.io/baseball/teams/43.png", },
      { id: 26, name: "Oakland Athletics", photo: "https://media.api-sports.io/baseball/teams/26.png", },
      { id: 27, name: "Philadelphia Phillies", photo: "https://media.api-sports.io/baseball/teams/27.png", },
      { id: 28, name: "Pittsburgh Pirates", photo: "https://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/pit.png&h=80&w=80&scale=crop&cquality=40&location=origin", },
      { id: 29, name: "Rochester Red Wings", photo: "https://media.api-sports.io/baseball/teams/29.png", },
      { id: 30, name: "San Diego Padres", photo: "https://media.api-sports.io/baseball/teams/30.png", },
      { id: 31, name: "San Francisco Giants", photo: "https://media.api-sports.io/baseball/teams/31.png", },
      { id: 32, name: "Seattle Mariners", photo: "https://media.api-sports.io/baseball/teams/32.png", },
      { id: 46, name: "Southeastern", photo: "https://media.api-sports.io/baseball/teams/46.png", },
      { id: 33, name: "St.Louis Cardinals", photo: "https://media.api-sports.io/baseball/teams/33.png", },
      { id: 34, name: "Tampa Bay Rays", photo: "https://media.api-sports.io/baseball/teams/34.png", },
      { id: 35, name: "Texas Rangers", photo: "https://media.api-sports.io/baseball/teams/35.png", },
      { id: 36, name: "Toronto Blue Jays", photo: "https://media.api-sports.io/baseball/teams/36.png", },
      { id: 37, name: "Washington Nationals", photo: "https://media.api-sports.io/baseball/teams/37.png" }
    ]
    this.team = this.teams[0];
    this.getAthletes();
  }

  ngOnInit(): void {
  }

  /**
   * Realiza el fitlrado de los atletas que correspondan con el texto capturada
   * @param search Texto o cadena a filtrar
   */
  getAthletes(search?: string): void {
    const data_1 = [
      { id: 1, photo: 'https://randomuser.me/api/portraits/men/3.jpg', name: 'juan', selected: false },
      { id: 2, photo: 'https://randomuser.me/api/portraits/men/89.jpg', name: 'Carlos', selected: false },
      { id: 3, photo: 'https://randomuser.me/api/portraits/men/50.jpg', name: 'Pepe', selected: false },
      { id: 4, photo: 'https://randomuser.me/api/portraits/men/39.jpg', name: 'Cristian', selected: false },
      { id: 5, photo: 'https://randomuser.me/api/portraits/men/43.jpg', name: 'Manuel', selected: false },
      { id: 6, photo: 'https://randomuser.me/api/portraits/men/13.jpg', name: 'Jose', selected: false },
      { id: 7, photo: 'https://randomuser.me/api/portraits/men/33.jpg', name: 'Mario', selected: false },
      { id: 8, photo: 'https://randomuser.me/api/portraits/men/18.jpg', name: 'Daniel', selected: false },
      { id: 9, photo: 'https://randomuser.me/api/portraits/men/83.jpg', name: 'Jorge', selected: false },
      { id: 10, photo: 'https://randomuser.me/api/portraits/men/56.jpg', name: 'Samuel', selected: false },
    ]
    const data_2 = [
      { id: 11, photo: 'https://randomuser.me/api/portraits/men/53.jpg', name: 'lorenzo', selected: false },
      { id: 12, photo: 'https://randomuser.me/api/portraits/men/85.jpg', name: 'Abif', selected: false },
      { id: 13, photo: 'https://randomuser.me/api/portraits/men/64.jpg', name: 'Angel', selected: false },
      { id: 14, photo: 'https://randomuser.me/api/portraits/men/91.jpg', name: 'Didier', selected: false },
      { id: 15, photo: 'https://randomuser.me/api/portraits/men/10.jpg', name: 'Gerardo', selected: false },
      { id: 16, photo: 'https://randomuser.me/api/portraits/men/9.jpg', name: 'Eduardo', selected: false },
      { id: 17, photo: 'https://randomuser.me/api/portraits/men/75.jpg', name: 'Omar', selected: false },
      { id: 18, photo: 'https://randomuser.me/api/portraits/men/23.jpg', name: 'Cesar', selected: false },
      { id: 19, photo: 'https://randomuser.me/api/portraits/men/95.jpg', name: 'Leonardo', selected: false },
      { id: 20, photo: 'https://randomuser.me/api/portraits/men/50.jpg', name: 'Fabian', selected: false },
    ]

    let data = (this.team.id % 2) ? data_1 : data_2;
    data = search ? data.filter(val => val.name.includes(search)) : data;

    this.athletes = data;
  }


  /**
   * Acciones a realizar por cada cambio en el checkbox de seleccionar todo.
   * @param change Datos de checkbox
   */
  onAthletesSelectAll(change: MatCheckboxChange): void {
    if (change.checked) {
      this.athletesList.selectAll();
    } else {
      this.athletesList.deselectAll();
    }
    this.assignUnassignAthletesToBlock();
  }

  /**
   * Acciones a realizar por cada cambio en la selección de atletas en la lista
   */
  onAthleteListSelectionChange(): void {
    this.assignUnassignAthletesToBlock();
  }

  private assignUnassignAthletesToBlock(): void {
    // if (!this.selectedBlock) {
    //   return;
    // }
    // //
    // this.setSelectAllChecked();
    // // Atletas asignados al bloque.
    // const selectedBlockAthletes = this.selectedBlockAthletes;
    // // Agrega o elimina atletas asignados al bloque según la selección actual de los atletas filtrados en la lista.
    // this.athletesList.options.forEach(option => {
    //   const athleteOption = option.value as Athlete;
    //   const athleteFound = selectedBlockAthletes.filter(athlete => athlete.id === athleteOption.id);
    //   // Si el atleta está seleccionado en la lista se agrega.
    //   // Siempre y cuando no esté ya agregado.
    //   if (option.selected) {
    //     if (!athleteFound.length) {
    //       selectedBlockAthletes.push(athleteOption);
    //     }
    //   }
    //   // Si el atleta en la lista NO está seleccionado se elimina de los atletas asignados al bloque.
    //   // Siempre y cuando esté asignado al atleta.
    //   else {
    //     if (athleteFound.length) {
    //       const index = selectedBlockAthletes.indexOf(athleteFound[0]);
    //       selectedBlockAthletes.splice(index, 1);
    //     }
    //   }
    // });
  }

}
