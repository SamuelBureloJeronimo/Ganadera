import { ResumeComponent } from './components/dashboard/admin/resume/resume.component';
import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LoginComponent } from './components/login/login.component';

export const routes: Routes = [
  { path: "", component: HomeComponent },
  { path: "login", component: LoginComponent },
  { path: "dashboard", component: DashboardComponent,
    children: [
      { path: "admin",
        children: [
          { path: "resume", component: ResumeComponent}
        ]}
    ]
   },
];
