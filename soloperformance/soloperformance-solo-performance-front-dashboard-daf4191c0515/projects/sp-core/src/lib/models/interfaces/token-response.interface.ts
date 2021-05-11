import { Permission } from './permission-response.interface';

export interface tokenResponse {
    access: string;
    refresh: string;
    permission: Permission;
    institution: number;
    subscription_active: boolean;
}