import { Injectable } from '@angular/core';
import { HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import * as moment from 'moment';

import { Periodicity, AuthService } from 'sp-core';

import { EventApp } from './../components/events/event-app.interface';
import { environment } from '@web/env/environment';
import { ApiService } from '@web/core/services/api.service';
import { EventResponse } from './../components/events/event-response.interface';
import { EventSummaryResponse } from './../models/interfaces/event-summary-response.interface';

@Injectable({
  providedIn: 'root'
})
export class EventService {

  constructor(
    private auth: AuthService,
    private api: ApiService
  ) { }

  getListByDate(
    date: Date,
    isMonth: boolean = false,
    teamId?: number,
    athleteId?: number
  ): Observable<Array<EventApp>> {

    let params = new HttpParams();
    params = params
      .set('type', isMonth ? '2' : '1')
      .set('institution', this.auth.institutionId.toString())
      .set('date', moment(date).format(environment.apiDateFormat));

    // Equipo
    if (teamId) {
      params = params.set('team', teamId.toString());
    }

    // Atleta
    if (athleteId) {
      params = params.set('athlete', athleteId.toString());
    }

    return this.api
      .get<Array<EventResponse>>('events-list/', params)
      .pipe(
        map(response => {
          const eventsApp: Array<EventApp> = [];
          response.forEach(responseItem => {
            eventsApp.push(<EventApp>{
              id: responseItem.id,
              name: responseItem.name,
              dateStart: moment(`${responseItem.date_start} ${responseItem.hour_start}`, 'YYYY-MM-DD HH:mm:ss', true).toDate(),
              dateEnd: moment(`${responseItem.date_end} ${responseItem.hour_end}`, 'YYYY-MM-DD HH:mm:ss', true).toDate()
            })
          })
          return eventsApp;
        }));
  }

  getSummaryByYear(
    year: number,
    teamId?: number,
    athleteId?: number
  ): Observable<Array<EventSummaryResponse>> {
    return this.getSummaryByPeriodicity(Periodicity.year, null, null, year, teamId, athleteId);
  }

  getSummaryByDates(
    date_begin: Date,
    date_end: Date,
    teamId?: number,
    athleteId?: number
  ): Observable<Array<EventSummaryResponse>> {
    return this.getSummaryByPeriodicity(Periodicity.month, date_begin, date_end, null, teamId, athleteId);
  }

  private getSummaryByPeriodicity(
    periodicity: Periodicity,
    date_begin?: Date,
    date_end?: Date,
    year?: number,
    teamId?: number,
    athleteId?: number
  ): Observable<Array<EventSummaryResponse>> {

    let params = new HttpParams();


    const type = (periodicity === Periodicity.year) ? 2 : 1;
    params = params.set('type', type.toString());

    // Institución
    params = params.set('institution', this.auth.institutionId.toString());

    // Rango de fechas/ año
    if (type === 2) {
      params = params.set('year', year.toString());
    } else {
      params = params
        .set('starts', moment(date_begin).format('YYYY-MM-DD'))
        .set('ends', moment(date_end).format('YYYY-MM-DD'));
    }

    // Equipo
    if (teamId) {
      params = params.set('team', teamId.toString());
    }

    // Atleta
    if (athleteId) {
      params = params.set('athlete', athleteId.toString());
    }

    return this.api.get<Array<EventSummaryResponse>>('events-filter/', params);
  }
}