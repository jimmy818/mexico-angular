import { Component, OnInit } from '@angular/core';
import { ApiService } from '@web/core/services/api.service';
import { ParamsService } from '@web/core/services/params.service';
import { PageConfig, PaginatorConfig } from 'sp-core';
import { Athletes, Data } from './athletes.interface';

@Component({
  selector: 'web-athletes',
  templateUrl: './athletes.component.html',
  styleUrls: ['./athletes.component.scss']
})
export class AthletesComponent implements OnInit {

  data: any[] = [];
  paginatorConfig: PaginatorConfig;
  columns: string[] = ['name', 'team', 'email', 'birth', 'weight', 'height', 'edit_at', 'actions'];

  constructor(
    private PRMS: ParamsService,
    private API: ApiService
  ) {
    this.PRMS.get.subscribe(() => {
      this.API.get(`athletes-library/?institution=48`, this.PRMS.params).subscribe((data: Data) => {
        this.data = data.data
        console.log(data);
        // this.data = [
        //   {
        //     id: 1,
        //     img: 'https://randomuser.me/api/portraits/men/1.jpg',
        //     name: 'carlos',
        //     team: 'chivas',
        //     email: 'carlos@yopmail.com',
        //     birth: '1995-05-22',
        //     weight: 80,
        //     height: 180,
        //     edit_at: { user: 'carlos', date: '2020-11-04' }
        //   },
        //   {
        //     id: 1,
        //     img: 'https://randomuser.me/api/portraits/men/2.jpg',
        //     name: 'juan',
        //     team: 'chivas',
        //     email: 'juan@yopmail.com',
        //     birth: '1995-05-22',
        //     weight: 80,
        //     height: 180,
        //     edit_at: { user: 'juan', date: '2020-11-04' }
        //   },
        //   {
        //     id: 1,
        //     img: 'https://randomuser.me/api/portraits/men/3.jpg',
        //     name: 'pedro',
        //     team: 'chivas',
        //     email: 'pedro@yopmail.com',
        //     birth: '1995-05-22',
        //     weight: 80,
        //     height: 180,
        //     edit_at: { user: 'pedro', date: '2020-11-04' }
        //   }
        // ]
        this.paginatorConfig = new PageConfig(data.pagination);
      });
    });
  }

  ngOnInit(): void {
  }

}
