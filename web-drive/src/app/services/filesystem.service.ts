import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CustomResponse } from '../models/custom-response.model';
import { UserService } from './user.service';

@Injectable({
  providedIn: 'root'
})
export class FilesystemService {

  URL_API = 'http://localhost:8000/fileSystem';

  sourcePath: string[] = [];
  moving: boolean = false;
  copying: boolean = false;
  name: string = "";

  constructor(private http:HttpClient, private _userService:UserService) { }

  async saveCopyInfo(name: string){
    let res:CustomResponse = (await this._userService.getUsersPaths().toPromise());
    this.sourcePath = res.response;
    this.name = name;
    this.copying = true;
  }

  async saveMoveInfo(name: string){
    let res:CustomResponse = (await this._userService.getUsersPaths().toPromise());
    this.sourcePath = res.response;
    this.name = name;
    this.moving = true;
  }

  copy():Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.post<CustomResponse>(`${this.URL_API}/copy`, {"user": userName, "sourcePaths": this.sourcePath, "name": this.name})
  }

  move():Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.post<CustomResponse>(`${this.URL_API}/move`, {"user": userName, "sourcePaths": this.sourcePath, "name": this.name})
  }

  cleanVariables(){
    this.copying = false;
    this.moving = false;
    this.name = "";
    this.sourcePath = []
  }

  isCopying():boolean{
    return this.copying;
  }

  isMoving():boolean{
    return this.moving;
  }
}
