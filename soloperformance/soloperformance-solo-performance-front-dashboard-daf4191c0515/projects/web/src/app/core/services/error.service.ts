import { Injectable } from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';
// import { UserService } from './user.service';
import { LoaderService } from './loader.service';
// import Swal from 'sweetalert2';
import { BehaviorSubject } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class ErrorService {

  // loader = new BehaviorSubject(null);

  constructor(
    public location: Location,
    // public userService: UserService,
    private loader: LoaderService,
    private RT: Router
  ) { }


  checkError(error: any): void {
    console.log(error)
    switch (error.status) {
      case 400:
        this.swal(error.error.mensaje);
        break;
      case 401:
        this.swal(error.error.error, true);
        break;
      case 404:
        this.RT.navigate(['404']);
        this.swal(error.error.mensaje);
        break;
      default:
        this.swal('Error de conexion');
        break;
    }
  }

  swal(msg: string, logout?: boolean): void {
    // Swal.fire({
    //   toast: true,
    //   position: 'top-end',
    //   type: 'error',
    //   title: msg,
    //   showConfirmButton: false,
    //   timer: 2500
    // })

    // this.location.back();
    // this.location.back();

    this.loader.status.next(false);

    // if (logout) {
    //   this.userService.logout();
    // }
  }

}
