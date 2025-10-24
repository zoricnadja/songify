import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RegisterComponent } from './auth/register/register.component';
import { HomeComponent } from './layout/home/home.component';
import { LoginComponent } from './auth/login/login.component';
import { AdminPanelComponent } from './admin/admin-panel/admin-panel.component';
import { SubscriptionsComponent } from './subscription/subscriptions/subscriptions.component';
import { AuthGuard } from './auth/auth.guard';
import { TrackPlayerListComponent } from './track/track-player-list/track-player-list.component';
import { DiscoverComponent } from './discover/discover/discover.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  {
    path: 'admin',
    component: AdminPanelComponent,
    canActivate: [AuthGuard],
    data: { role: ['admin'] },
  },
  {
    path: 'subscriptions',
    component: SubscriptionsComponent,
    canActivate: [AuthGuard],
    data: { role: ['user'] },
  },
  {
    path: 'tracks',
    component: TrackPlayerListComponent,
    canActivate: [AuthGuard],
    data: { role: ['user', 'admin'] },
  },
  {
    path: 'discover',
    component: DiscoverComponent,
    canActivate: [AuthGuard],
    data: { role: ['user', 'admin'] },
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
