import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-create-folder',
  templateUrl: './create-folder.component.html',
  styleUrls: ['./create-folder.component.scss']
})
export class CreateFolderComponent implements OnInit {

  name: string = "Ejemplo.txt";
  form!: FormGroup;

  constructor(
    private readonly _fb: FormBuilder
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
        name: ['', [Validators.required, Validators.pattern(/\w*/)]],
      }
    )
  }

}
