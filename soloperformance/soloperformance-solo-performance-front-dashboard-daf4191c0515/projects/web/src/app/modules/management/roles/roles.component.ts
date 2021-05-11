import { Component, OnInit } from '@angular/core';
import { ApiService } from '@web/core/services/api.service';
import { ParamsService } from '@web/core/services/params.service';
import { PaginatorConfig, PageConfig } from 'sp-core';
import { Data, Roles } from './roles.interface'

@Component({
  selector: 'web-roles',
  templateUrl: './roles.component.html',
  styleUrls: ['./roles.component.scss']
})
export class RolesComponent implements OnInit {

  data: Roles[] = [];
  paginatorConfig: PaginatorConfig;
  columns: string[] = ['name', 'team', 'email', 'rol', 'phone', 'edit_at', 'actions'];

  constructor(
    private PRMS: ParamsService,
    private API: ApiService
  ) {
    this.PRMS.get.subscribe(() => {
      this.API.get(`users-library/?institution=48`, this.PRMS.params).subscribe((data: Data) => {
        this.data = data.data;
        this.paginatorConfig = new PageConfig(data.pagination);
      });
    });
  }

  ngOnInit(): void {
  }

}
