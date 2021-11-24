import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { User } from 'src/app/models/user.model';
import { FilesService } from 'src/app/services/files.service';
import { FolderService } from 'src/app/services/folders.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-choose-shared',
  templateUrl: './choose-shared.component.html',
  styleUrls: ['./choose-shared.component.scss']
})
export class ChooseSharedComponent implements OnInit {

  users!:User[];
  form = new FormControl();


  constructor(
    private readonly _usersService: UserService,
    private readonly _fb: FormBuilder,
    private readonly _fileService: FilesService,
  ) { }

  async ngOnInit():Promise<void> {
    this.users = (await this._usersService.getUsers().toPromise()).response;
    
  }

  get userInvalid(){
    return this.form.get('user')?.invalid && this.form.get('user')?.touched
  }

}
