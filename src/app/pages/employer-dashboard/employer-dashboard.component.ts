import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-employer-dashboard',
  standalone: true,
  imports: [],
  templateUrl: './employer-dashboard.component.html',
  styleUrl: './employer-dashboard.component.css'
})
export class EmployerDashboardComponent {
  user: any = null;

  constructor(private router: Router) {
    const raw = localStorage.getItem('currentUser');
    this.user = raw ? JSON.parse(raw) : null;

    if (!this.user || this.user.role !== 'employer') {
      this.router.navigate(['/login']);
    }
  }

  logout(): void {
    localStorage.removeItem('currentUser');
    this.router.navigate(['/home']);
  }
}