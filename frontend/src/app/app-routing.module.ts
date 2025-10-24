import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RegisterComponent } from './auth/register/register.component';
import { HomeComponent } from './layout/home/home.component';
import { LoginComponent } from './auth/login/login.component';
import { AdminPanelComponent } from './admin/admin-panel/admin-panel.component';
import { SubscriptionsComponent } from './subscription/subscriptions/subscriptions.component';
import { TrackPlayerListComponent } from './track/track-player-list/track-player-list.component';
import { DiscoverComponent } from './discover/discover/discover.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'admin', component: AdminPanelComponent },
  { path: 'subscriptions', component: SubscriptionsComponent },
  { path: 'tracks', component: TrackPlayerListComponent },
  { path: 'discover', component: DiscoverComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
