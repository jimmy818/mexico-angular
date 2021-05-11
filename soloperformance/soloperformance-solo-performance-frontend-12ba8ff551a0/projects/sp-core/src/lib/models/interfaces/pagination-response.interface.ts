import { PaginationLinkResponse } from './pagination-link-response.interface';

export interface PaginationResponse {
    total_rows: number;
    per_page: number;
    current_page: number;
    links: PaginationLinkResponse;
}