import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { AuthService } from '../../auth/auth.service';
import { LoginComponent } from '../../auth/login/login.component';
import { OnInit } from '@angular/core';

@Component({
  selector: 'app-navbar',
  standalone: false,
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss',
})
export class NavbarComponent implements OnInit {
  isModalOpen = false;
  role: string | null = '';
  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.authService.role$.subscribe((role) => {
      this.role = role;
    });
  }

  logout(): void {
    this.authService.logout().then(() => {
      this.authService.loadRole();
    });
  }
}
