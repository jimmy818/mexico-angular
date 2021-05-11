import { PaginationResponse } from './pagination-response.interface';

export interface PaginatorConfig {
  length: number;
  pageSize: number;
  pageIndex: number;
  pageSizeOptions: Array<number>;
}

export class PageConfig {
  length: number;
  pageSize: number;
  pageIndex: number;
  pageSizeOptions: Array<number>;

  constructor(pagination: PaginationResponse) {
    this.length = pagination.total_rows;
    this.pageSize = Number(pagination.per_page);
    this.pageIndex = pagination.current_page;
    this.pageSizeOptions = [5, 10, 25, 100];
  }
}
