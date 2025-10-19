import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { MaterialModule } from '../infrastructure/material/material.module';
import { ReactiveFormsModule } from '@angular/forms';
import { VerifyComponent } from './verify/verify.component';
import { RouterModule } from '@angular/router';
@NgModule({
  declarations: [LoginComponent, RegisterComponent, VerifyComponent],
  imports: [CommonModule, MaterialModule, ReactiveFormsModule, RouterModule],
})
export class AuthModule {}
