import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';


import {AppComponent} from "./app.component";
import {LandComponent} from "./land.component";
import {AnalyzeComponent} from "./analyze.component";
import {routing} from "./app.routing";
import {FormsModule} from "@angular/forms";
import {HttpModule} from "@angular/http";
import {InterComponent} from "./inter.component";
//import {KeyWord} from "./keyword.service";


// Import HttpClientModule from @angular/common/http


@NgModule({
    declarations: [AppComponent,
        LandComponent,
        AnalyzeComponent,
        InterComponent
        ],
    imports: [BrowserModule,
        routing,
        FormsModule,
        HttpModule,
        BrowserModule,

    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule {

}