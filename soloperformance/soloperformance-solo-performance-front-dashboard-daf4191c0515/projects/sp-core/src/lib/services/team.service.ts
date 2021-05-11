import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import * as moment_ from 'moment';
const moment = moment_;

import { AuthService } from './auth.service';

import { RequestParam } from './../models/interfaces/request-param.interface';
import { UserType } from '../models/enums/user-type.enum';
import { TEAM_PARAM_NAMES } from '../constants/team-param-names.constants';
import { Teams } from '../models/interfaces/teams.interface';
import { TeamsResponse } from './../models/interfaces/teams-response.interface';
import { Team } from '../models/interfaces/team.interface';
import { User } from '../models/interfaces/user.interface';
import { InstitutionManager } from '../models/interfaces/institution-manager.interface';
import { Pagination } from '../models/pagination.model';
import { Institution } from '../models/interfaces/institution.interface';
import { AthletesResponse } from '../models/interfaces/athletes-response.interface';
import { Athletes } from '../models/interfaces/athletes.interface';
import { Athlete } from '../models/interfaces/athlete.interface';
import { TeamUserType } from '../models/enums/team-user-type.enum';
import { AthleteResponse } from '../models/interfaces/athlete-response.interface';

@Injectable({
  providedIn: 'root'
})
export class TeamService {

  constructor(
    private http: HttpClient,
    private auth: AuthService
  ) { }

  /**
   * Obtiene la lista de equipos correspondientes a la institución del usuario en sesión.
   * @param search Filtro de búsqueda
   */
  getList(
    search?: string
  ): Observable<Teams> {

    // Filtros o parámetros.
    let httpParams = new HttpParams()
      .set(TEAM_PARAM_NAMES.institutionId, this.auth.institutionId.toString())

    // Filtro de búsqueda.
    if (search) {
      httpParams = httpParams.set(TEAM_PARAM_NAMES.search, search);
    }

    const options = {
      params: httpParams
    }

    return this.http
      .get<TeamsResponse>('teams-catalog/', options)
      .pipe(
        map(response => {

          const teams: Array<Team> = [];
          response.data.forEach(teamResponse => {
            const team = <Team>{
              id: teamResponse.id,
              name: teamResponse.name,
              image: teamResponse.image,
              isActive: teamResponse.active,
              updatedBy: <User>{
                id: teamResponse.updated_by.id,
                photo: teamResponse.updated_by.photo,
                fullName: teamResponse.updated_by.full_name
              },
              createdAt: moment(teamResponse.created_at, false).toDate(),
              updatedAt: moment(teamResponse.updated_at, false).toDate(),
              institution: <Institution>{
                id: teamResponse.institution
              }
            };
            teamResponse.institution_managers.forEach(manager => {
              team.institutionManagers = [];
              team.institutionManagers.push(<InstitutionManager>{
                id: manager.id,
                photo: manager.photo,
                fullName: manager.full_name
              })
            })
            teams.push(team);
          });

          return <Teams>{
            data: teams,
            pagination: Pagination.mapToModel(response.pagination)
          };
        }));
  }

  addAthlete(
    teamId: number,
    athleteId: number
  ): Observable<any> {

    const body = {
      type: 1,
      team: teamId,
      user: athleteId
    }

    return this.http.post('current-user-team/', body);
  }

  /**
   * Obtiene la lista de atletas del equipo indicado
   * @param teamId Identificador de equipo
   */
  getAthletes(
    teamId: number
  ): Observable<Array<Athlete>> {

    // Filtros o parámetros.
    let httpParams = new HttpParams()
      .set('type', TeamUserType.athlete.toString());

    const options = {
      params: httpParams
    }

    return this.http
      .get<Array<AthleteResponse>>(`current-user-team/${teamId.toString()}/`, options)
      .pipe(map(response => {

        const athletes: Array<Athlete> = [];
        response.forEach(athleteResponse => {
          athletes.push(<Athlete>{
            id: athleteResponse.id,
            fullName: athleteResponse.full_name,
            email: athleteResponse.email,
            birthdate: moment(athleteResponse.birthday, false).toDate()
          });
        })

        return athletes;
      }));
  }

  getUsers(
    params?: Array<RequestParam>
  ): Observable<any> {

    // Filtros o parámetros.
    let httpParams = new HttpParams();
    if (params) {
      params.forEach(filter => {
        httpParams = httpParams.set(filter.key, filter.value);
      });
    }

    const options = {
      params: httpParams
    }

    return this.http.get('user-team/', options);
  }
}