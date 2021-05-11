import { PaginationResponse } from 'sp-core';

export interface LastEdited {
  id: number;
  photo?: string;
  full_name: string;
}

export interface Roles {
  id: number;
  full_name: string;
  email: string;
  photo: string;
  birthday?: Date;
  type: number;
  last_edited: LastEdited;
  updated_at: Date;
  is_active: boolean;
}

export class Data {
  data: Roles[];
  pagination: PaginationResponse
}
