import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import * as moment from 'moment';

import { RequestParam } from 'sp-core';

import { environment } from '@admin/env/environment';
import { Institution } from '@admin/shared/models/institution.model';
import { InstitutionsDto } from '@admin/shared/models-dto/institutions-dto.model';
import { InstitutionCreateDto } from '@admin/shared/models-dto/institution-create-dto.model';
import { InstitutionCreateResponseDto } from '@admin/shared/models-dto/institution-create-response-dto.model';
import { InstitutionDetailResponse } from '@admin/shared/models-dto/institution-detail-response.model';

@Injectable({
  providedIn: 'root'
})
export class InstitutionService {

  private apiBaseURL = environment.apiBaseUrl;

  constructor(
    private http: HttpClient
  ) { }


  /**
   * Obtiene información referente a institución
   * @param institutionId Identificador de institución
   */
  getInfo(
    institutionId: number
  ): Observable<InstitutionDetailResponse> {
    return this.http.get<InstitutionDetailResponse>(`${this.apiBaseURL}info-institution/${institutionId.toString()}/`);
  }

  getList(
    params?: Array<RequestParam>
  ): Observable<InstitutionsDto> {

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

    return this.http.get<InstitutionsDto>(`${this.apiBaseURL}institution-list/`, options);
  }

  /**
   * Crea una nueva institución
   * @param institution Datos de institución
   */
  create(institution: Institution): Observable<InstitutionCreateResponseDto> {

    // Institution/User/Account
    const institutionDto: InstitutionCreateDto = {
      name: institution.name,
      active: institution.isActive,
      identifier_name: institution.dbName,
      type: institution.type,
      ends: moment(institution.expirationDate).format('YYYY-MM-DD'),
      total_athletes: institution.totalAthletes,
      total_coaches: institution.totalCoaches,
      total_team: institution.totalTeams,
      total: institution.total,
      tax: institution.tax,
      price: institution.price,
      fee_stripe: institution.stripeFee,
      has_renewable: institution.hasRenewable
    };

    return this.http.post<InstitutionCreateResponseDto>(`${this.apiBaseURL}institution/`, institutionDto);
  }
}