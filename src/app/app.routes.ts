import { Routes } from '@angular/router';
import { SplashScreenComponent } from './pages/splash-screen/splash-screen.component';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { WorkerDashboardComponent } from './pages/worker-dashboard/worker-dashboard.component';
import { EmployerDashboardComponent } from './pages/employer-dashboard/employer-dashboard.component';
import { ResumeFormComponent } from './pages/resume-form/resume-form.component';
import { MyResumesComponent } from './pages/my-resumes/my-resumes.component';

export const routes: Routes = [
  { path: '', component: SplashScreenComponent },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },

  { path: 'worker', component: WorkerDashboardComponent },
  { path: 'worker/resume/create', component: ResumeFormComponent },
  { path: 'worker/resumes', component: MyResumesComponent },

  { path: 'employer', component: EmployerDashboardComponent },

  { path: '**', redirectTo: '' }
];