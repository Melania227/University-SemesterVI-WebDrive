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


  createUser(user: User):Observable<CustomResponse>{
    return this.http.post<CustomResponse>(this.URL_API, user)
  }


  private getlogIn(userName: string):Observable<CustomResponse>{
    return this.http.post<CustomResponse>(this.URL_API + "/logIn", {"user": userName})
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
}
