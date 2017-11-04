import {Component, OnInit} from '@angular/core';
import {SafeUrl} from "@angular/platform-browser";
import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer} from '@angular/platform-browser';

import {Http} from "@angular/http";
import {Observable} from "rxjs/Observable";

const json = require('./test.json');


@Component({
    selector: 'my-app',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})


export class AppComponent{


    /*
    video: SafeUrl = "https://www.youtube.com/embed/EF8UnVXj0gY";


    constructor(private sanitizer: DomSanitizer) {

    }
    public getSantizeUrl(url : string) {
        return this.sanitizer.bypassSecurityTrustUrl(url);
    }
*/
    blank_context_url = "http://blank.org/";
    first_context_url = "https://en.wikipedia.org/wiki/Naturalistic Imperative";
    second_context_url = "https://en.wikipedia.org/wiki/Mitochondrion";
    third_context_url = "https://en.wikipedia.org/wiki/Brain";
    context_current_url: SafeUrl;

    init_url = "https://www.youtube.com/embed/EF8UnVXj0gY";
    first_url = "https://www.youtube.com/embed/EF8UnVXj0gY?start=60&autoplay=1";
    second_url = "https://www.youtube.com/embed/EF8UnVXj0gY?start=80&autoplay=1";
    third_url = "https://www.youtube.com/embed/EF8UnVXj0gY?start=100&autoplay=1";
    current_url: SafeUrl;

    constructor(private sanitizer: DomSanitizer) {
        this.current_url=this.sanitizer.bypassSecurityTrustResourceUrl(this.init_url);
        this.context_current_url=this.sanitizer.bypassSecurityTrustResourceUrl(this.blank_context_url)
        console.log(json)
    }

    updateSrc(url) {
        this.current_url=this.sanitizer.bypassSecurityTrustResourceUrl(url)
    }

    updateContext(url) {
        this.context_current_url=this.sanitizer.bypassSecurityTrustResourceUrl(url)
    }

    /*slide variables for location */

    /*slide one */
    firstid_first = "first_slide_first_element";
    slide_one_first_url = this.first_url;
    slide_one_second_url = this.second_url;
    slide_one_third_url = this.third_url;

    slide_one_first_context_url = this.first_context_url;
    slide_one_second_context_url = this.second_context_url;
    slide_one_third_context_url = this.third_context_url;

    first_el_y = json.frame_one.keyword_one.key_one_y;
    first_el_x = json.frame_one.keyword_one.key_one_x;
    first_el_fs = 20;

    sec_el_y = 130;
    sec_el_x = 40;
    sec_el_fs = 14;
    sec_el_wid = 150;

    sectwo_el_y = 150;
    sectwo_el_x = 40;
    sectwo_el_fs = 14;
    sectwo_el_wid = 150;

    thir_el_y = 80;
    thir_el_x = 200;

    first_img_url = "https://upload.wikimedia.org/wikipedia/commons/e/e8/Figure_35_03_03.png";
    first_img_wid = 240;
    first_img_hei = 180



}

export class APPComponentJSON{
    data;

    constructor(private http:Http) {
        this.http.get('../Test.json')
            .subscribe(res => this.data = res.json());
        console.log(this.data)
    }


}


