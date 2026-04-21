import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  method = 'other';
  login = '';
  password = '';
  role = 'worker';
  name = '';
  surname = '';
  patronymic = '';
  email = '';
  phone = '';
  address = '';
  company = '';
  error = '';

  methods = [
    { id: 'google', label: 'Google' },
    { id: 'icloud', label: 'iCloud' },
    { id: 'phone', label: 'Телефон' },
    { id: 'other', label: 'Другие' }
  ];

  constructor(private router: Router, private api: ApiService) {}

  async submit(): Promise<void> {
    this.error = '';

    try {
      const user = await this.api.post('/register/', {
        method: this.method,
        login: this.login,
        password: this.password,
        role: this.role,
        name: this.name,
        surname: this.surname,
        patronymic: this.patronymic,
        email: this.email,
        phone: this.phone,
        address: this.address,
        company: this.company
      });

      localStorage.setItem('currentUser', JSON.stringify(user));

      if (user.role === 'worker') {
        this.router.navigate(['/worker']);
      } else {
        this.router.navigate(['/employer']);
      }
    } catch (e: any) {
      this.error = e.message || 'Ошибка регистрации';
    }
  }
}