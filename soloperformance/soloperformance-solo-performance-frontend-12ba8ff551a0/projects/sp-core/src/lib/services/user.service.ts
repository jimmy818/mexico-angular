import { Injectable } from '@angular/core';
import { HttpParams, HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import * as moment_ from 'moment';
const moment = moment_;

import { RequestParam } from './../models/interfaces/request-param.interface';
import { Users } from './../models/interfaces/users.interface';
import { User } from './../models/interfaces/user.interface';
import { UserPostRequest } from './../models/interfaces/user-post-request.interface';

import { UserResponse } from './../models/interfaces/user-response.interface';
import { UserType } from '../models/enums/user-type.enum';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(
    private http: HttpClient
  ) { }

  /**
   * Obtiene lista de usuarios.
   * TODO: Se inició el desarrollo para obtener los atletas pero se indicó que es otro servicio el que devuelve dicha información. Se agrega al servicio de team.service.
   */
  get(
    params?: Array<RequestParam>
  ): Observable<Users> {

    // Filtros o parámetros.
    let httpParams = new HttpParams();
    if (params) {
      params.forEach(filter => {
        httpParams = httpParams.set(filter.key, filter.value);
      })
    }

    const options = {
      params: httpParams
    }

    return null;

    // return this.http
    //   .get<UsersResponse>('user/', options)
    //   .pipe(
    //     map(response => {

    //     }));
  }

  /**
   * Agrega/crea un nuevo atleta a la institución. TODO: Realizar pruebas.
   * @param user Datos de usuario atleta
   */
  createAthlete(
    user: User
  ): Observable<UserResponse> {

    const body: UserPostRequest = {
      full_name: user.fullName,
      email: user.email,
      password: user.password,
      confirm_password: user.password,
      country_code: user.countryCode,
      birthday: moment(user.birthdate).format('YYYY-MM-DD'),
      photo: user.photo,
      phone: user.phone,
      type: UserType.athlete,
      region: user.region,
      gender: user.gender,
      heigth: user.height,
      weigth: user.weight,
      institution: user.institution.id
    };

    return this.http.post<UserResponse>('users/', body);
  }

  /**
   * Agrega/crea un nuevo strenght coach a la institución. TODO: Realizar pruebas
   * @param user Datos de usuario
   */
  createCoach(
    user: User
  ): Observable<UserResponse> {

    const body: UserPostRequest = {
      full_name: user.fullName,
      email: user.email,
      password: user.password,
      confirm_password: user.password,
      country_code: user.countryCode,
      birthday: moment(user.birthdate).format('YYYY-MM-DD'),
      photo: user.photo,
      phone: user.phone,
      type: UserType.strengthCoach,
      region: user.region,
      gender: user.gender,
      heigth: user.height,
      weigth: user.weight,
      institution: user.institution.id
    };

    return this.http.post<UserResponse>('users/', body);
  }

  /**
   * Agrega/crea un nuevo institution manager a la institución. TODO: Realizar pruebas
   * @param user Datos de usuario
   */
  createInstitutionManager(
    user: User
  ): Observable<UserResponse> {

    const body: UserPostRequest = {
      full_name: user.fullName,
      email: user.email,
      password: user.password,
      confirm_password: user.password,
      country_code: user.countryCode,
      birthday: moment(user.birthdate).format('YYYY-MM-DD'),
      photo: user.photo,
      phone: user.phone,
      type: UserType.institutionManager,
      region: user.region,
      gender: user.gender,
      heigth: user.height,
      weigth: user.weight,
      team: user.team.id,
      institution: user.institution.id
    };

    return this.http.post<UserResponse>('users/', body);
  }

}
