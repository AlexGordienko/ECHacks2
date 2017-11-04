/**
 * Created by alexgordienko on 2017-11-04.
 */
import {RouterModule, Routes} from "@angular/router";

const APP_ROUTES: Routes = [
    { path: 'views/index.hbs', redirectTo: '/assessment', pathMatch: 'full' },
];

export const routing = RouterModule.forRoot(APP_ROUTES);