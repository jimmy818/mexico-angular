import { Component, OnInit } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';

import { AuthService, UserInfo } from 'sp-core';
import { HeaderGroupAlignment } from 'sp-library';

@Component({
  selector: 'admin-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  userInfo: UserInfo;

  headerGroupAlignment = HeaderGroupAlignment;

  logo = 'assets/images/solo-performance.svg';

  constructor(
    private matIconRegistry: MatIconRegistry,
    private domSanitizer: DomSanitizer,
    private router: Router,
    private authService: AuthService
  ) {
    this.matIconRegistry.addSvgIcon('logo', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/images/solo-performance.svg'));
    this.matIconRegistry.addSvgIcon('settings', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/settings.svg'));
    this.matIconRegistry.addSvgIcon('notifications', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/bell.svg'));
    this.matIconRegistry.addSvgIcon('photo', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/example-photo.svg'));
    this.matIconRegistry.addSvgIcon('expand', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/expand.svg'));
    this.matIconRegistry.addSvgIcon('logout', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/keyboard-backspace.svg'));
  }

  ngOnInit(): void {
    this.authService
      .getUserInfo()
      .subscribe(data => {
        this.userInfo = data;
      });
  }

  logout() {
    this.authService.logout().subscribe(result => {
      this.router.navigate(['/auth'], { replaceUrl: true });
    })
  }
}
