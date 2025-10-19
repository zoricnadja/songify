import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';
import { NavbarComponent } from './navbar/navbar.component';
import { MaterialModule } from '../infrastructure/material/material.module';
import { MenuComponent } from './menu/menu.component';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [HomeComponent, NavbarComponent, MenuComponent],
  imports: [CommonModule, MaterialModule, RouterModule],
  exports: [NavbarComponent],
})
export class LayoutModule {}
