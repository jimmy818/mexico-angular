import { Component, ContentChildren, Input, AfterContentInit, QueryList, ViewChild } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatColumnDef, MatTable } from '@angular/material/table';
import { Router } from '@angular/router';
import { merge } from 'rxjs';
import { startWith, switchMap } from 'rxjs/operators';
import { PAGE_SIZE_OPTIONS, PaginatorConfig } from 'sp-core';

@Component({
  selector: 'web-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss']
})
export class TableComponent<T> implements AfterContentInit {

  @Input() paginatorConfig: PaginatorConfig = {} as PaginatorConfig;
  @Input() data: Array<T> = [];
  @Input() columns: Array<string> = [];
  @Input() footer: boolean;

  // this is where the magic happens:
  @ViewChild(MatTable, { static: true }) table: MatTable<T>;
  @ContentChildren(MatColumnDef) columnDefs: QueryList<MatColumnDef>;

  @ViewChild(MatSort) sort: MatSort;

  constructor(
    private RT: Router
  ) {
    console.log(this.RT['rawUrlTree']['queryParams']);
    // if (this.RT['rawUrlTree']['queryParams']['page'] != undefined) {
    //   this.paginatorConfig.pageIndex = Number(this.RT['rawUrlTree']['queryParams']['page']) - 1
    // }
  }

  // after the <ng-content> has been initialized, the column definitions are available.
  // All that's left is to add them to the table ourselves:
  ngAfterContentInit() {
    // console.log(this.columnDefs);
    // console.log(this.table);


    this.columnDefs.forEach(columnDef => this.table.addColumnDef(columnDef));

    // // Si se cambia el ordenamiento se cambia a la primera página.
    // setTimeout(() => {
    //   this.sort.sortChange.subscribe(() =>
    //     console.log(this.sort)
    //   );
    // });
    // if (this.sort.active && this.sort.direction) {
    //   console.log(this.sort);
    //   // const sortDirection = this.sort.direction === 'asc' ? REQUEST_PARAM_NAMES.orderAsc : REQUEST_PARAM_NAMES.orderDesc;
    //   // params.push({ key: REQUEST_PARAM_NAMES.sort, value: `${sortDirection}${this.sort.active}` });
    // }

    // Si se cambia el ordenamiento se cambia a la primera página.
    // this.sort.sortChange.subscribe(() => this.paginator.pageIndex = 0);
  }

  setPage(event: PaginatorConfig): void {
    console.log(event);
    let queryParams: { per_page: number, page: number };
    queryParams = {
      // si el tamaño de la pagina es diferente al default lo agrega sino lo quita
      per_page: event.pageSize != 10 ? event.pageSize : null,
      // si la pagina es diferente a 1 la agrega sino lo quita
      page: event.pageIndex != 0 ? event.pageIndex + 1 : null,
    }

    const urlTree = this.RT.createUrlTree([], {
      queryParams: queryParams,
      queryParamsHandling: "merge",
      preserveFragment: true
    });
    this.RT.navigateByUrl(urlTree);
  }

  sortData(event: any): void {
    console.log(event);
  }

  showUserDetail(event: any) {
    console.log(event);
  }

}
