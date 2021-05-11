import { Gender } from '../enums/gender.enum';
import { UserType } from '../enums/user-type.enum';
import { Team } from './team.interface';
import { Institution } from './institution.interface';

export interface User {
    id: number;
    type: UserType,
    fullName: string;
    email?: string;
    isActive?: boolean;
    username?: string;
    password?: string;
    emailVerified?: boolean;
    height?: number;
    weight?: number;
    gender?: Gender;
    photo?: string;
    region?: number,
    countryCode?: number;
    phone?: string;
    birthdate?: string;
    team?: Team;
    institution?: Institution;
}