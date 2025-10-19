import { Injectable } from '@angular/core';
import {
  signUp,
  signIn,
  signOut,
  fetchAuthSession,
  getCurrentUser,
  confirmSignUp,
  resendSignUpCode,
} from 'aws-amplify/auth';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor() {}

  async register(user: any) {
    return await signUp({
      username: user.username,
      password: user.password,
      options: {
        userAttributes: {
          email: user.email,
          birthdate: user.birthdate,
          given_name: user.givenName,
          family_name: user.familyName,
          'custom:role': user.role,
        },
      },
    });
  }

  async login(username: string, password: string) {
    return await signIn({ username: username, password });
  }

  async logout() {
    return await signOut();
  }

  async getUser() {
    const user = await getCurrentUser();
    return user;
  }

  async getToken() {
    const session = await fetchAuthSession();
    return session.tokens?.idToken?.toString();
  }

  async confirmSignUp(username: string, code: string) {
    try {
      await confirmSignUp({
        username: username,
        confirmationCode: code,
      });
      console.log('User confirmed successfully!');
    } catch (error) {
      console.error('Error confirming sign up:', error);
    }
  }

  async resendCode(username: string) {
    try {
      await resendSignUpCode({ username: username });
      console.log('Confirmation code resent');
    } catch (err: any) {
      console.log(err.message || 'Error resending code');
    }
  }
}
