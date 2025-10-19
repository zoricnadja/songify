import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../auth/auth.service';
import { MenuItem } from './menu-item.model';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.scss',
  standalone: false,
})
export class MenuComponent {
  menuItems: MenuItem[] = [{ path: '/', label: 'Home', roles: true }];
  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  hasRole(requiredRoles: string[] | true): boolean {
    if (requiredRoles == true) return true;
    if (!this.authService.getUser) return false;
    return true;
    // return requiredRoles.includes(this.authService.getUser);
  }
}
