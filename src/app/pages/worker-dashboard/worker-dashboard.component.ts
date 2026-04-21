import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-worker-dashboard',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './worker-dashboard.component.html',
  styleUrl: './worker-dashboard.component.css'
})
export class WorkerDashboardComponent {
  user: any = null;

  constructor(private router: Router) {
    const raw = localStorage.getItem('currentUser');
    this.user = raw ? JSON.parse(raw) : null;

    if (!this.user || this.user.role !== 'worker') {
      this.router.navigate(['/login']);
    }
  }

  logout(): void {
    localStorage.removeItem('currentUser');
    this.router.navigate(['/home']);
  }
}