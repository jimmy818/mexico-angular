import { User } from './user.interface';
import { InstitutionManager } from './institution-manager.interface';
import { Athlete } from './athlete.interface';
import { Coach } from './coach.interface';
import { Institution } from './institution.interface';

export interface Team {
    id: number;
    name: string;
    image: string;
    isActive: boolean;
    institution: Institution;
    updatedBy?: User;
    institutionManagers?: Array<InstitutionManager>;
    athletes?: Array<Athlete>;
    coaches?: Array<Coach>;
    createdAt?: Date;
    updatedAt?: Date;
}