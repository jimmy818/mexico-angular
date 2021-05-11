import { AfterViewInit, Component, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { merge, of, Subject } from 'rxjs';
import { catchError, finalize, map, startWith, switchMap } from 'rxjs/operators';

import { PAGE_SIZE_OPTIONS, PaginatorConfig, RequestParam, REQUEST_PARAM_NAMES } from 'sp-core';
import { HeaderGroupAlignment } from 'sp-library';

import { InstitutionDto } from '@admin/shared/models-dto/institution-dto.model';

import { InstitutionService } from '../../services/institution.service';

@Component({
  selector: 'admin-institution-list',
  templateUrl: './institution-list.component.html',
  styleUrls: ['./institution-list.component.scss']
})
export class InstitutionListComponent implements OnInit, AfterViewInit {

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  @Output() addUser = new EventEmitter<null>();
  @Output() showDetail = new EventEmitter<InstitutionDto>();

  paginatorConfig: PaginatorConfig;

  headerGroupAlignment = HeaderGroupAlignment;

  institutionsDC: string[] = ['id', 'name', 'subscription', 'created_at', 'active', 'net_revenue', 'actions'];

  institutions: Array<InstitutionDto> = [];

  private searchText = '';
  private search = new Subject<null>();

  constructor(
    private institutionService: InstitutionService
  ) {
    this.paginatorConfig = <PaginatorConfig>{
      length: 0,
      pageSize: 10, // Por defecto tamaño de página 10
      pageIndex: 0, // Por defecto la primera página
      pageSizeOptions: PAGE_SIZE_OPTIONS
    }
  }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {

    // Si se cambia el ordenamiento se cambia a la primera página.
    this.sort.sortChange.subscribe(() => this.paginator.pageIndex = 0);

    // Si se realiza una búsqueda se cambia a la primera página.
    this.search.subscribe(() => this.paginator.pageIndex = 0);

    // Escucha cada cambio en paginación, ordenamiento y búsqueda.
    merge(this.sort.sortChange, this.paginator.page, this.search)
      .pipe(
        startWith({}),
        switchMap(() => {
          const params: Array<RequestParam> = [];
          if (this.sort.active && this.sort.direction) {
            const sortDirection = this.sort.direction === 'asc' ? REQUEST_PARAM_NAMES.orderAsc : REQUEST_PARAM_NAMES.orderDesc;
            params.push({ key: REQUEST_PARAM_NAMES.sort, value: `${sortDirection}${this.sort.active}` });
          }
          if (this.searchText) {
            params.push({ key: REQUEST_PARAM_NAMES.search, value: this.searchText });
          }
          // Página: +1: Debido a que el control de angular material inicia en cero la paginación.
          if ((this.paginator.pageIndex + 1)) {
            params.push({ key: REQUEST_PARAM_NAMES.page, value: (this.paginator.pageIndex + 1).toString() });
          }
          if (this.paginator.pageSize) {
            params.push({ key: REQUEST_PARAM_NAMES.pageSize, value: this.paginator.pageSize.toString() });
          }
          // Obtiene datos paginados.
          return this.institutionService.getList(params);
        }),
        map(data => {
          this.paginator.length = data.pagination.total_rows;
          return data.data
        }),
        catchError(error => {
          return of([]);
        }),
        finalize(() => {

        }),
      ).subscribe(data => {
        this.institutions = data;
      });
  }

  onNewUser(): void {
    this.addUser.emit();
  }

  showUserDetail(institution: InstitutionDto): void {
    this.showDetail.emit(institution);
  }

  onSearchEnter(text: string): void {
    this.searchText = text;
    this.search.next();
  }

  onSearchClearText(): void {
    this.searchText = '';
    this.search.next();
  }
}
