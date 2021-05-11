import { PaginationLinkDto } from './pagination-link-dto.model';

export interface PaginationDto {
    total_rows: number;
    per_page: number;
    current_page: number;
    links: PaginationLinkDto;
}