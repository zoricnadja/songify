import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';
import { inject } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  standalone: false,
})
export class LoginComponent {
  loginForm: FormGroup;
  loginError: string | null = null;
  loading = false;
  snackBar: MatSnackBar = inject(MatSnackBar);

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  async onSubmit() {
    this.loginError = null;
    this.loading = true;

    if (this.loginForm.valid) {
      const { username, password } = this.loginForm.value;
      try {
        await this.authService.login(username, password);
        this.authService.loadRole();
        this.router.navigate(['/home']);
      } catch (error: any) {
        this.loginError = error.message || 'An unexpected error occurred during login.';
        console.error('Login failed:', error);
      } finally {
        this.loading = false;
      }
    }
  }
}
