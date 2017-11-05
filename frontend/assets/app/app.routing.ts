/**
 * Created by alexgordienko on 2017-11-04.
 */
import {RouterModule, Routes} from "@angular/router";
import {AppComponent} from "./app.component";
import {LandComponent} from "./land.component";
import {AnalyzeComponent} from "./analyze.component";
import {InterComponent} from "./inter.component";


const APP_ROUTES: Routes = [
    { path: 'views/index.hbs', redirectTo: '/analyze', pathMatch: 'full' },
    { path: '', redirectTo: '/analyze', pathMatch: 'full' },
    { path: 'analyze', component: AnalyzeComponent },
    { path: 'landing', component: LandComponent },
    { path: 'inter', component: InterComponent },
];

export const routing = RouterModule.forRoot(APP_ROUTES);