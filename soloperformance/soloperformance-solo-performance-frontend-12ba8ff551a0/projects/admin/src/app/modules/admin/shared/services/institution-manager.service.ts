import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import * as moment from 'moment';

import { UserType } from 'sp-core';

import { UserCreateResponseDto } from '@admin/shared/models-dto/user-create-response-dto.model';
import { environment } from '@admin/env/environment';
import { InstitutionManager } from '@admin/shared/models/institution-manager.model';
import { UserCreateDto } from '@admin/shared/models-dto/user-create-dto.model';

@Injectable({
  providedIn: 'root'
})
export class InstitutionManagerService {

  private apiBaseURL = environment.apiBaseUrl;

  constructor(
    private http: HttpClient
  ) { }

  create(
    manager: InstitutionManager,
    teamId: number,
    institutionId: number
  ): Observable<UserCreateResponseDto> {

    // Administrador de institución
    const userBody: UserCreateDto = {
      full_name: `${manager.name} ${manager.lastname}`,
      email: manager.email,
      password: manager.password,
      confirm_password: manager.passwordConfirm,
      country_code: 52,// TODO: Definir si se captura
      phone: manager.phone,
      birthdate: moment(manager.birthdate).format('YYYY-MM-DD'),
      photo: null,
      type: UserType.institutionManager,
      region: 1, // TODO: Verificar si se pide al usuario.
      gender: manager.gender,
      team: teamId,
      institution: institutionId
    };

    return this.http.post<UserCreateResponseDto>(`${this.apiBaseURL}users/`, userBody);
  }
}
