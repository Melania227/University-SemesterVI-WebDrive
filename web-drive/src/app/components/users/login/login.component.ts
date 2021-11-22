import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { CustomResponse } from 'src/app/models/custom-response.model';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
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

  createForm(){
    this.form = this._fb.group(
      {
        username: ['', [Validators.required]]
      }
    )
  }

  async login(){
    if (this.form.valid){
      let res:CustomResponse = (await this._userService.logIn(this.form.get("username")?.value));
      if(res.error){
        console.log(res.response);
        this._snackBar.open(res.response, "Ok", {
          duration: 3000,
          panelClass: ['custom-class'],
        });
      }
      else{
        //this._router.navigateByUrl(`invoices-list`);
        console.log(res.response);
      }
    }
  }

}
