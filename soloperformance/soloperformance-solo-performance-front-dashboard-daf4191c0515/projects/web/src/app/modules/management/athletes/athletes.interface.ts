import { PaginationResponse } from 'sp-core';

export interface Team {
  id: number;
  name: string;
}

export interface Athletes {
  id: number;
  full_name: string;
  email: string;
  photo?: string;
  birthday?: Date;
  weigth: string;
  heigth: string;
  phone?: string;
  last_edited?: any;
  updated_at: Date;
  is_active: boolean;
  teams: Team[];
}

export class Data {
  data: Athletes[];
  pagination: PaginationResponse
}
