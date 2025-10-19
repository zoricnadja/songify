import { Component, inject } from '@angular/core';
import { AuthService } from '../auth.service';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  FormBuilder,
  ValidationErrors,
  Validators as AngularValidators,
} from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: false,
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
})
export class RegisterComponent {
  registerForm: FormGroup;
  registerError: string | null = null;
  loading = false;
  snackBar: MatSnackBar = inject(MatSnackBar);

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.registerForm = this.fb.group(
      {
        username: ['', AngularValidators.required],
        email: ['', [AngularValidators.required, AngularValidators.email]],
        password: ['', [AngularValidators.required, AngularValidators.minLength(8)]],
        confirmPassword: ['', AngularValidators.required],
        givenName: [''],
        familyName: [''],
        birthdate: [''],
        role: ['user'],
      },
      { validators: passwordMatchValidator }
    );
  }

  async onSubmit() {
    this.registerError = null;
    this.loading = true;

    if (this.registerForm.valid) {
      const { username, email, password, givenName, familyName, birthdate, role } =
        this.registerForm.value;
      const user = { username, email, password, givenName, familyName, birthdate, role };
      try {
        await this.authService.register(user);
        this.snackBar.open('Registration successful!', 'OK', { duration: 3000 });
        this.router.navigate(['/verify']);
      } catch (error: any) {
        this.registerError = error.message || 'An unexpected error occurred during registration.';
        console.error('Registration failed:', error);
      } finally {
        this.loading = false;
      }
    }
  }
}

export const passwordMatchValidator = (control: AbstractControl): ValidationErrors | null => {
  const password = control.get('password');
  const confirmPassword = control.get('confirmPassword');
  return password && confirmPassword && password.value !== confirmPassword.value
    ? { mismatch: true }
    : null;
};
