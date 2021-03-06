import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { User } from '../models/user.model';
import { Observable } from 'rxjs';
import { CustomResponse } from '../models/custom-response.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  URL_API = 'http://localhost:8000/users';

  constructor(private http:HttpClient) { }


  createUser(userName: string, maxBytes: number):Observable<CustomResponse>{
    return this.http.post<CustomResponse>(this.URL_API, {"user": userName, "maxBytes": maxBytes})
  }


  private getlogIn(userName: string):Observable<CustomResponse>{
    return this.http.post<CustomResponse>(`${this.URL_API}/logIn`, {"user": userName})
  }

  async logIn(userName: string): Promise<CustomResponse>{

    let res: CustomResponse = (await this.getlogIn(userName).toPromise())
    
    if (!res.error){
      localStorage.setItem('user', userName);
    }

    return res
  }

  logOut(){
    localStorage.removeItem('user');
  }

  cleanPaths():Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.post<CustomResponse>(`${this.URL_API}/cleanPaths`, {"user": userName})
  }

  getCurrentStorage():Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.get<CustomResponse>(`${this.URL_API}/storage/?user=${userName}`);
  }

  getUsers():Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.get<CustomResponse>(`${this.URL_API}/?user=${userName}`);
  }

  getUsersPaths():Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.get<CustomResponse>(`${this.URL_API}/paths/?user=${userName}`); 
  }
}
