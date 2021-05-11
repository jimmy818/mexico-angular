export interface EventResponse {
    id: number;
    name: string;
    hour_start: string;
    hour_end: string;
    date_start: string;
    date_end: string;
    team: Array<number>;
    athletes: Array<number>;
}