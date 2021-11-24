import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  constructor(
    private readonly _router: Router,
    private readonly _userService: UserService

  ) { }

  ngOnInit(): void {
  }

  logout(){
    this._userService.logOut();
    this._router.navigateByUrl("login");
  }

}
