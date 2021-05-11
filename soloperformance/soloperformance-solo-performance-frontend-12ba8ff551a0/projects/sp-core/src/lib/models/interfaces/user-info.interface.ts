import { Gender } from '../enums/gender.enum';
import { UserType } from '../enums/user-type.enum';

export interface UserInfo {
    id: number;
    type: UserType;
    region: number;
    fullName: string;
    countryCode: number;
    phone: string;
    gender: Gender;
    birthdate: Date;
    photo: string;
    email: string;
    username: string;
    emailVerified: boolean;
    isSubscriptionActive: boolean;
    isActive: boolean;
    teamId: number;
    institutionId: number;
}