/**
 * Created by alexgordienko on 2017-11-05.
 */
import {Component, Input} from '@angular/core';
import {FormControl, Validators} from '@angular/forms';
import {NgForm} from '@angular/forms';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import { Http, Response, Headers } from "@angular/http";
import 'rxjs/Rx';
import {VidForm} from "./land.model";
import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {Observable} from "rxjs/Observable";

// Import HttpClientModule from @angular/common/http


@Component({
    selector: 'my-land',
    templateUrl: './land.component.html',
    styleUrls: ['./analyze.component.css']
})


export class LandComponent{
    constructor(private http:Http) { }

    vidForm: VidForm = new VidForm();
    results: string;


    onSubmit(f:NgForm) {
        console.log(f["link"]);
        // const body = JSON.stringify(this.vidForm);// convert the form to a JSON string.
        // const headers = new Headers({'content-type':'application/json'});// server receives headers that the the form is type JSON
        // this.http.post('/assessment', body, {headers:headers}).subscribe(data=>{//post the form to /assessment/business where it can be picked up by backend
        //         console.log(data);
        //     },);
        this.http.get('http://192.168.8.147:5000/new-video/'+ f["link"] + '/lecture1').subscribe(data => {
            // Read the result field from the JSON response.
            //this.results = data['results'];
            console.log(data)
        });
        // this.http.get('http://192.168.8.147:5000/get-data/lecture1')
        //     .subscribe(res => { console.log(res.text()) });
        // const headers = new Headers({'Access-Control-Allow-Origin': 'http://localhost:3000'});// server receives headers that the the form is type JSON
        // this.http.get('http://192.168.8.147:5000/get-data/lecture1', {headers:headers}).subscribe(data=>{//post the form to /assessment/business where it can be picked up by backend
        //         console.log(data.text());
        //     },);
        // this.http
        //     .get('http://192.168.8.147:5000/new-video/lecture1')
        //     .map(this.extractData)
        //     .catch(this.handleError);
        this.http.request('http://192.168.8.147:5000/get-data/lecture1')
            .map(res => res.json())
            .subscribe(data => {
                this.results = data;

                console.log(this.results);
            })


    }
    //
    // private extractData(res: Response) {
    //     let body = res.text();  // If response is a JSON use json()
    //     console.log(body);
    //     if (body) {
    //         return body;
    //     } else {
    //         return {};
    //     }
    // }
    //
    // private handleError(error: any) {
    //     // In a real world app, we might use a remote logging infrastructure
    //     // We'd also dig deeper into the error to get a better message
    //     let errMsg = (error.message) ? error.message :
    //         error.status ? `${error.status} - ${error.statusText}` : 'Server error';
    //     console.error(errMsg); // log to console instead
    //     return Observable.throw(errMsg);
    // }
    /*
    constructor(private http:Http) { }

    onSubmit(f: NgForm){

        const body = JSON.stringify(this.businessForm);// convert the form to a JSON string.
        const headers = new Headers({'content-type':'application/json'});// server receives headers that the the form is type JSON
        this.http.post('/assessment/business', body, {headers:headers}).subscribe(data=>{//post the form to /assessment/business where it can be picked up by backend
            if(this.eligibility == true){
                this.isSubmitted = true;
                this.isSubmittedInEligible = false;
            }
            else {
                this.isSubmittedInEligible = true;
                this.isSubmitted = false;
            }
            this.isError = false;
            this.businessForm.fullName = "";
            console.log(data);
        },

    }
     */
}