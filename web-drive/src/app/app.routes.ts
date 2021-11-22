import { RouterModule, Routes } from "@angular/router";
import { LoginComponent } from "./components/users/login/login.component";
import { SignUpComponent } from "./components/users/sign-up/sign-up.component";


const APP_ROUTES : Routes = [
    {path: 'login', component: LoginComponent},
    {path: 'sign-up', component: SignUpComponent},
    {path: '**', pathMatch: 'full', redirectTo: 'login'} /* PREDETERMINADA */
];

export const APP_ROUTING = RouterModule.forRoot(APP_ROUTES, {useHash:true});