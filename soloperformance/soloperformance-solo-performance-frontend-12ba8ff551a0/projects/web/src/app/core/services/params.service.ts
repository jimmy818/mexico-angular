import { Injectable } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { HttpParams } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class ParamsService {

  get = new BehaviorSubject(null);
  params: HttpParams;

  constructor(
    private RT: Router,
    private AR: ActivatedRoute,
  ) {
    this.AR.queryParams.subscribe(
      (params: Params) => {
        console.log(params);

        let prms: HttpParams = new HttpParams()
        Object.keys(params).forEach(function(key) {
          prms = prms.append(key, params[key]);
        });
        this.params = prms;
        this.get.next(true);
      }
    );
  }

  set(prms: { hey: string, value: string }) {
    const urlTree = this.RT.createUrlTree([], {
      queryParams: prms,
      queryParamsHandling: "merge",
      preserveFragment: true
    });
    this.RT.navigateByUrl(urlTree);
  }
}
