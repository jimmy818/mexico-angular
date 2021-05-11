export interface EventApp {
    id: number;
    name: string;
    dateStart: Date;
    dateEnd: Date;
    teamIds: Array<number>;
    athleteIds: Array<number>;
}