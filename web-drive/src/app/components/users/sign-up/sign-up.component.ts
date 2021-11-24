import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { CustomResponse } from 'src/app/models/custom-response.model';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss']
})
export class SignUpComponent implements OnInit {
  form!: FormGroup;

  constructor(
    private readonly _fb: FormBuilder,
    private readonly _userService: UserService,
    private _snackBar: MatSnackBar,
    private readonly _router: Router
  ) { }

  ngOnInit(): void {
    this.createForm();
  }

  get usernameInvalid(){
    return this.form.get('username')?.invalid && this.form.get('username')?.touched
  }
  get maxBytesInvalid(){
    return this.form.get('username')?.invalid && this.form.get('username')?.touched
  }

  createForm(){
    this.form = this._fb.group(
      {
        username: ['', [Validators.required]],
        maxBytes: ['', [Validators.required, Validators.pattern(/\d+/)]]
      }
    )
  }

  async signUp(){
    if (this.form.valid){
      let res = (await this._userService.createUser(this.form.get("username")?.value, this.form.get("maxBytes")?.value).toPromise());
      if(res.error){
        this._snackBar.open(res.response, "Ok", {
          duration: 3000,
          panelClass: ['error-class'],
        });
      }
      else{
        this._snackBar.open(res.response, "Ok", {
          duration: 3000,
          panelClass: ['success-class'],
        });
        this._router.navigateByUrl(`home`);
      }
    }
  }

}
