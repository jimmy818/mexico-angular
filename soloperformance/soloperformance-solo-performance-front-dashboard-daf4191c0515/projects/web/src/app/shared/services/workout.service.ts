import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { ApiService } from '@web/core/services/api.service';

import { BlockCoding, BlockType } from '../models';
import { BlockCodingResponse } from '../models/interfaces/block-coding-response.interface';
import { BlockTypeResponse } from '../models/interfaces/block-type-response.interface';

@Injectable({
  providedIn: 'root'
})
export class WorkoutService {

  constructor(
    private api: ApiService
  ) { }

  getBlockCodings(): Observable<Array<BlockCoding>> {
    return this.api
      .get<Array<BlockCodingResponse>>('coding/')
      .pipe(
        map(response => {
          const blockCodings = response.map(codingResponse => BlockCoding.fromResponse(codingResponse));
          return blockCodings.sort((a, b) => a.id - b.id);
        })
      );
  }

  getBlockTypes(): Observable<Array<BlockType>> {
    return this.api
      .get<Array<BlockTypeResponse>>('blocktypes/')
      .pipe(
        map(response => {
          return response.map(blockTypeResponse => BlockType.fromResponse(blockTypeResponse));
        })
      )
  }
}