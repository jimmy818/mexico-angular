import { PaginationResponse } from 'sp-core';

export interface InstitutionManager {
  id: number;
  photo?: string;
  full_name: string;
}

export interface Athlete {
  id: number;
  photo?: string;
  full_name: string;
}

export interface Coach {
  id: number;
  photo?: any;
  full_name: string;
}

export interface UpdatedBy {
  id: number;
  photo?: string;
  full_name: string;
}

export interface Team {
  id: number;
  institution_managers: InstitutionManager[];
  athletes: Athlete[];
  coaches: Coach[];
  updated_by: UpdatedBy;
  name: string;
  image: string;
  active: boolean;
  created_at: Date;
  updated_at: Date;
  institution: number;
}

export class Data {
  data: Team[];
  pagination: PaginationResponse
}
