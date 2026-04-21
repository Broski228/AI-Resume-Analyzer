import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-my-resumes',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './my-resumes.component.html',
  styleUrl: './my-resumes.component.css'
})
export class MyResumesComponent {
  user: any = null;
  resumes: any[] = [];

  constructor(private router: Router, private api: ApiService) {
    const raw = localStorage.getItem('currentUser');
    this.user = raw ? JSON.parse(raw) : null;

    if (!this.user || this.user.role !== 'worker') {
      this.router.navigate(['/login']);
    } else {
      this.load();
    }
  }

  async load(): Promise<void> {
    this.resumes = await this.api.get(`/workers/${this.user.id}/resumes/`);
  }
}