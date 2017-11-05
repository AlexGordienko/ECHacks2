/**
 * Created by alexgordienko on 2017-11-05.
 */
import {Component} from '@angular/core';
import {Observable} from 'rxjs/Rx';
import {Http} from "@angular/http";


@Component({
    selector: 'my-inter',
    templateUrl: './inter.component.html',
    styleUrls: ['./inter.component.css']
})


export class InterComponent{
    results: string;
    constructor(private http:Http){
        Observable.interval(100 * 60).subscribe(x => {
            window.location.reload();
        });
        this.http.request('http://192.168.8.147:5000/get-data/lecture1')
            .map(res => res.json())
            .subscribe(data => {
                this.results = data;
                console.log(this.results);
            })
    }

}