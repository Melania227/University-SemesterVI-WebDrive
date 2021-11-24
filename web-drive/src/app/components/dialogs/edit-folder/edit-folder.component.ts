import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Folder } from 'src/app/models/folder.model';

@Component({
  selector: 'app-edit-folder',
  templateUrl: './edit-folder.component.html',
  styleUrls: ['./edit-folder.component.scss']
})
export class EditFolderComponent implements OnInit {

  name: string = "Ejemplo.txt";
  form!: FormGroup;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data:Folder,
    private readonly _fb: FormBuilder,
  ) { }

  ngOnInit(): void {
    this.createForm();
  }

  get nameInvalid(){
    return this.form.get('name')?.invalid && this.form.get('name')?.touched
  }

  createForm(){
    this.form = this._fb.group(
      {
        name: [this.data.name, [Validators.required, Validators.pattern(/\w*/)]],
      }
    )
  }

}
