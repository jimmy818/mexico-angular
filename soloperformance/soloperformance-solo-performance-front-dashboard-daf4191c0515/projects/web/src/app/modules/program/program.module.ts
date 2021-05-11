import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProgramComponent } from './program.component';
import { SharedModule } from '@web/shared/shared.module';
import { RouterModule } from '@angular/router';
import { ImgsModule } from '@web/shared/components/imgs/imgs.module';
import { MenuTopModule } from './menu/menu-top/menu-top.module';
import { MenuLeftModule } from './menu/menu-left/menu-left.module';
import { MenuRightModule } from './menu/menu-right/menu-right.module';
import { CalendarProgramModule } from './calendar/calendar.module';
import { SpDialogModule } from 'sp-dialog';
import { DialogsModule } from './dialogs/dialogs.module';


@NgModule({
  declarations: [ProgramComponent],
  imports: [
    RouterModule.forChild([{ path: '', component: ProgramComponent }]),
    CommonModule,
    SharedModule,
    ImgsModule,
    MenuTopModule,
    MenuLeftModule,
    MenuRightModule,
    CalendarProgramModule,
    SpDialogModule,
    DialogsModule
  ]
})
export class ProgramModule { }
