import { Component, OnInit } from '@angular/core';
import { ApiService } from '@web/core/services/api.service';
import { ParamsService } from '@web/core/services/params.service';
import { PageConfig, PaginatorConfig } from 'sp-core';
import { Data, Team } from './teams.interface';

@Component({
  selector: 'web-teams',
  templateUrl: './teams.component.html',
  styleUrls: ['./teams.component.scss']
})
export class TeamsComponent implements OnInit {

  data: Team[] = [];
  paginatorConfig: PaginatorConfig;
  columns: string[] = ['name', 'coaches', 'athletes', 'edit_at', 'actions'];

  constructor(
    private PRMS: ParamsService,
    private API: ApiService
  ) {
    this.PRMS.get.subscribe(() => {
      this.API.get(`teams-catalog/`, this.PRMS.params).subscribe((data: Data) => {
        this.data = data.data;
        this.paginatorConfig = new PageConfig(data.pagination);
      });
    });
  }

  ngOnInit(): void {
  }
}
