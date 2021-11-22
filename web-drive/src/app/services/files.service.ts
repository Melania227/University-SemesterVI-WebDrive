import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CustomResponse } from '../models/custom-response.model';

@Injectable({
  providedIn: 'root'
})
export class FilesService {

  URL_API = 'http://localhost:8000/files';

  constructor(private http:HttpClient) { }

  createFile(fileName: string, data: string):Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.post<CustomResponse>(this.URL_API, {"user": userName, "name": fileName, "data": data});
  }

  getFile(fileName: string):Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.get<CustomResponse>(`${this.URL_API}/?user=${userName}&name=${fileName}`);
  }

  deleteFile(fileName: string):Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.delete<CustomResponse>(`${this.URL_API}/?user=${userName}&name=${fileName}`);
  }

  updateFile(originalName: string, newName: string, newData: string):Observable<CustomResponse>{
    let userName = localStorage.getItem('user');
    return this.http.patch<CustomResponse>(this.URL_API, {"user": userName, "name": originalName, "newName": newName, "newData": newData});
  }
}
