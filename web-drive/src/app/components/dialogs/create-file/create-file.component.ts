import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { File } from 'src/app/models/file.model';
import { FilesService } from 'src/app/services/files.service';

@Component({
  selector: 'app-create-file',
  templateUrl: './create-file.component.html',
  styleUrls: ['./create-file.component.scss']
})
export class CreateFileComponent implements OnInit {

  name: string = "Ejemplo.txt";
  form!: FormGroup;


  constructor(
    private readonly _fb: FormBuilder,
    private _snackBar: MatSnackBar,
    @Inject(MAT_DIALOG_DATA) public data:File,
    private readonly _fileService: FilesService
  ) { }

  ngOnInit(): void {
    this.createForm();
  }

  get nameInvalid(){
    return this.form.get('name')?.invalid && this.form.get('name')?.touched
  }

  get contentInvalid(){
    return this.form.get('content')?.invalid && this.form.get('content')?.touched
  }

  createForm(){
    this.form = this._fb.group(
      {
        name: ['', [Validators.required, Validators.pattern(/\w*/)]],
        content: ['', [Validators.required, Validators.pattern(/\w*/)]]
      }
    )
  }

}
