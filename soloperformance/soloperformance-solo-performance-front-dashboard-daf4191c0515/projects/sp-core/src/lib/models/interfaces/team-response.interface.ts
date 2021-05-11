import { InstitutionManagerResponse } from './institution-manager-response.interface';
import { AthleteResponse } from './athlete-response.interface';
import { CoachResponse } from './coach-response.interface';
import { UserResponse } from './user-response.interface';

export interface TeamResponse {
  id: number;
  institution_managers: Array<InstitutionManagerResponse>;
  athletes: Array<AthleteResponse>;
  coaches: Array<CoachResponse>;
  updated_by: UserResponse;
  name: string;
  image: string;
  active: boolean;
  created_at: Date;
  updated_at: Date;
  institution: number;
}