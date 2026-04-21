import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  login = '';
  password = '';
  error = '';

  constructor(private router: Router, private api: ApiService) {}

  async submit(): Promise<void> {
    this.error = '';

    try {
      const user = await this.api.post('/login/', {
        login: this.login,
        password: this.password
      });

      localStorage.setItem('currentUser', JSON.stringify(user));

      if (user.role === 'worker') {
        this.router.navigate(['/worker']);
      } else {
        this.router.navigate(['/employer']);
      }
    } catch (e: any) {
      this.error = e.message || 'Ошибка входа';
    }
  }
}