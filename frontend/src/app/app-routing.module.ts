import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RegisterComponent } from './auth/register/register.component';
import { HomeComponent } from './layout/home/home.component';
import { LoginComponent } from './auth/login/login.component';
import { AdminPanelComponent } from './admin/admin-panel/admin-panel.component';
import { SubscriptionsComponent } from './subscription/subscriptions/subscriptions.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'admin', component: AdminPanelComponent },
  { path: 'subscriptions', component: SubscriptionsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
