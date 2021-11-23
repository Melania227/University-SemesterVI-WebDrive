import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { File } from 'src/app/models/file.model';
import { FilesService } from 'src/app/services/files.service';

@Component({
  selector: 'app-edit-file',
  templateUrl: './edit-file.component.html',
  styleUrls: ['./edit-file.component.scss']
})
export class EditFileComponent implements OnInit {

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
        name: [this.data.name, [Validators.required, Validators.pattern(/\w*/)]],
        content: [this.data.data, [Validators.required, Validators.pattern(/\w*/)]]
      }
    )
  }

  async editFile(){
    let res = (await this._fileService.updateFile(this.data.name, this.form.get("name")?.value, this.form.get("content")?.value).toPromise());
    if(res.error){
      console.log(res.response)
      this._snackBar.open(res.response, "Ok", {
        duration: 3000,
        panelClass: ['error-class'],
      });
    }
    else{
      console.log(res.response)
      this._snackBar.open(res.response, "Ok", {
        duration: 3000,
        panelClass: ['success-class'],
      });
    }
  }

}
