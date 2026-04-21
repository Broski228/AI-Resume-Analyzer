import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';


@Component({
  selector: 'app-resume-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './resume-form.component.html',
  styleUrl: './resume-form.component.css'
})
export class ResumeFormComponent {
  user: any = null;
  error = '';

  specialty = 'programmer';
  level = 'Junior';
  experience = '0';
  country = 'Қазақстан';
  city = 'Алматы';
  bachelor = 'no';
  bachelorUniversity = '';
  bachelorYears = '';
  masters = 'no';
  mastersUniversity = '';
  mastersYears = '';
  workplace = '';
  hasProjects = 'no';
  projectLink = '';
  languages: string[] = [];
  about = '';
  photo = '';

  specialties: Record<string, string[]> = {
    programmer: ['Junior', 'Middle', 'Senior', 'Team Lead'],
    teacher: ['Педагог', 'Педагог-модератор', 'Педагог-эксперт', 'Педагог-шебер']
  };

  cities = ['Алматы', 'Астана', 'Шымкент', 'Қарағанды'];
  years = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10+'];
  universities = ['KBTU', 'AITU', 'Satbayev University', 'Al-Farabi KazNU', 'ENU'];
  studyYears = ['2015 - 2019', '2016 - 2020', '2017 - 2021', '2018 - 2022', '2019 - 2023', '2020 - 2024'];
  languageOptions = ['Қазақша', 'Русский', 'English', 'Türkçe'];

  constructor(private router: Router, private api: ApiService) {
    const raw = localStorage.getItem('currentUser');
    this.user = raw ? JSON.parse(raw) : null;

    if (!this.user || this.user.role !== 'worker') {
      this.router.navigate(['/login']);
    }
  }

  setDefaultLevel(): void {
    this.level = this.specialties[this.specialty][0];
  }

  toggleLanguage(language: string): void {
    if (this.languages.includes(language)) {
      this.languages = this.languages.filter(item => item !== language);
    } else {
      this.languages = [...this.languages, language];
    }
  }

  async save(): Promise<void> {
    try {
      await this.api.post('/resumes/create/', {
        worker: this.user.id,
        photo: this.photo,
        specialty: this.specialty,
        level: this.level,
        experience: this.experience,
        country: this.country,
        city: this.city,
        bachelor: this.bachelor === 'yes',
        bachelor_university: this.bachelorUniversity,
        bachelor_years: this.bachelorYears,
        masters: this.masters === 'yes',
        masters_university: this.mastersUniversity,
        masters_years: this.mastersYears,
        workplace: this.workplace,
        has_projects: this.hasProjects === 'yes',
        project_link: this.projectLink,
        languages: this.languages,
        about: this.about
      });

      this.router.navigate(['/worker/resumes']);
    } catch (e: any) {
      this.error = e.message || 'Ошибка сохранения';
    }
  }
}