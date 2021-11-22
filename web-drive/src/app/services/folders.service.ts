import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Observable } from 'rxjs';
import { CustomResponse } from '../models/custom-response.model';

@Injectable({
  providedIn: 'root'
})
export class FolderService {

  URL_API = 'http://localhost:8000/folders';

  constructor(private http:HttpClient) { }

  openFolder(folderName: string):Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.post<CustomResponse>(`${this.URL_API}/open`, {"user": userName, "name": folderName});
  }

  closeFolder(folderName: string):Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.post<CustomResponse>(`${this.URL_API}/close`, {"user": userName, "name": folderName});
  }

  goToFolder(paths: string[], position: number):Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.post<CustomResponse>(`${this.URL_API}/goTo`, {"user": userName, "paths": paths.slice(0, position+1)});
  }

  getCurrentFolder():Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.get<CustomResponse>(`${this.URL_API}/current/?user=${userName}`);
  }

  createFolder(folderName: string):Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.post<CustomResponse>(this.URL_API, {"user": userName, "name": folderName});
  }

  deleteFolder(folderName: string):Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.delete<CustomResponse>(`${this.URL_API}/?user=${userName}&name=${folderName}`);
  }

  updateFolderName(originalName: string, newName: string):Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.patch<CustomResponse>(this.URL_API, {"user": userName, "name": originalName, "newName": newName});
  }
}
