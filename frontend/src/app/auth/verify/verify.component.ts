import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-verify',
  standalone: false,
  templateUrl: './verify.component.html',
  styleUrl: './verify.component.scss',
})
export class VerifyComponent {
  confirmForm: FormGroup;
  confirmationError = '';

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) {
    this.confirmForm = this.fb.group({
      username: ['', Validators.required],
      code: ['', Validators.required]
    });
  }

  onConfirm() {
    const { username, code } = this.confirmForm.value;
    this.authService.confirmSignUp(username, code);
    this.router.navigate(['/login']);
  }

  async resendCode() {
    const username = this.confirmForm.get('username')?.value;
    if (!username) return;
    this.authService.resendCode(username);
  }
}
