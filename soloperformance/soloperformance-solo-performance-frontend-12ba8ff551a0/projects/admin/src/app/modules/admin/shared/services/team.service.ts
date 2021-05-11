import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '@admin/env/environment';
import { Team } from '@admin/shared/models/team.model';
import { TeamCreateResponseDto } from '@admin/shared/models-dto/team-create-response-dto.model';
import { TeamCreateDto } from '@admin/shared/models-dto/team-create-dto.model';

@Injectable({
  providedIn: 'root'
})
export class TeamService {

  private apiBaseURL = environment.apiBaseUrl;

  constructor(
    private http: HttpClient
  ) { }

  create(
    team: Team,
    institutionId: number
  ): Observable<TeamCreateResponseDto> {

    // Team
    const teamBody: TeamCreateDto = {
      name: team.name,
      institution: institutionId
    };

    return this.http.post<TeamCreateResponseDto>(`${this.apiBaseURL}teams/`, teamBody);
  }
}
