import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatMenuTrigger } from '@angular/material/menu';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Folder } from 'src/app/models/folder.model';
import { FilesService } from 'src/app/services/files.service';
import { FolderService } from 'src/app/services/folders.service';
import { CreateFolderComponent } from '../dialogs/create-folder/create-folder.component';
import { EditFileComponent } from '../dialogs/edit-file/edit-file.component';
import { EditFolderComponent } from '../dialogs/edit-folder/edit-folder.component';
import { OpenFileComponent } from '../dialogs/open-file/open-file.component';
import { CreateFileComponent } from '../dialogs/create-file/create-file.component';
import { UserService } from 'src/app/services/user.service';
import { ChooseSharedComponent } from '../dialogs/choose-shared/choose-shared.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  folder!: any;
  paths: string[]=[];

  @ViewChild(MatMenuTrigger) contextMenu!: MatMenuTrigger;

  contextMenuPosition = { x: '0px', y: '0px' };

  constructor(
    private readonly _folderService: FolderService,
    private readonly _fileService: FilesService,
    private readonly _userService: UserService,
    private _openDialog: MatDialog,
    private _snackBar: MatSnackBar
  ) { }

  async ngOnInit():Promise<void> {
    this.folder = (await this._folderService.openFolder('root').toPromise()).response;
    this.paths.push('root');
  }

  onContextMenu(event: MouseEvent, item: (File|Folder)) {
    event.preventDefault();
    this.contextMenuPosition.x = event.clientX + 'px';
    this.contextMenuPosition.y = event.clientY + 'px';
    this.contextMenu.menuData = { 'item': item };
    this.contextMenu.menu.focusFirstItem('mouse');
    this.contextMenu.openMenu();
  }

  async onContextMenuOpen(item: (File|Folder)) {
    if(item.type==="file"){
      let info = (await this._fileService.getFile(item.name).toPromise()).response;
      this._openDialog.open(OpenFileComponent, {width: '1000px', data: info});
    }
    else{
      this.folder = (await this._folderService.openFolder(item.name).toPromise()).response;
      this.paths.push(item.name);
    }
  }

  onContextMenuEdit(item: (File|Folder)) {
    if (item.type!=="file"){
      alert(`Edit name of ${item.name}`);
    }
    else{
      alert(`Edit ${item.name}`);
    }
  }

  onContextMenuCopy(item: (File|Folder)) {
    alert(`Copy ${item.name}`);
  }

  onContextMenuMove(item: (File|Folder)) {
    alert(`Move ${item.name}`);
  }

  onContextMenuShare(item: (File|Folder)){
    let done = this._openDialog.open(ChooseSharedComponent, {width: '1000px'}).afterClosed();
    done.subscribe(async (res)=>{
      let res2 = item.type==='file'?(await this._fileService.shareFile(item.name,res.user).toPromise()):(await this._folderService.shareFolder(item.name,res.user).toPromise());
      if(res2.error){
        this._snackBar.open(res2.response, "Ok", {
          duration: 3000,
          panelClass: ['error-class'],
        });
      }
      else{
        this.folder = (await this._folderService.getCurrentFolder().toPromise()).response;
        this._snackBar.open(res2.response, "Ok", {
          duration: 3000,
          panelClass: ['success-class'],
        });
      }
    });
  }

  onContextMenuAddFile(){
    alert(`Create File`);
  }

  onContextMenuAddFolder(){
    alert(`Create Folder`);
  }

  async editFile(item: File){
    let info = (await this._fileService.getFile(item.name).toPromise()).response;
    let done = this._openDialog.open(EditFileComponent, {width: '1000px', data: info}).afterClosed();
    done.subscribe(async (res)=>{
      let res2 = (await this._fileService.updateFile(item.name, res.name, res.content).toPromise());
      if(res2.error){
        this._snackBar.open(res2.response, "Ok", {
          duration: 3000,
          panelClass: ['error-class'],
        });
      }
      else{
        this.folder = (await this._folderService.getCurrentFolder().toPromise()).response;
        this._snackBar.open(res2.response, "Ok", {
          duration: 3000,
          panelClass: ['success-class'],
        });
      }
    });
  }

  async editFolder(item: Folder){
    let done = this._openDialog.open(EditFolderComponent, {width: '1000px', data: item}).afterClosed();
    done.subscribe(async (res)=>{
      let res2 = (await this._folderService.updateFolderName(item.name, res.name).toPromise());
      if(res2.error){
        this._snackBar.open(res2.response, "Ok", {
          duration: 3000,
          panelClass: ['error-class'],
        });
      }
      else{
        this.folder = (await this._folderService.getCurrentFolder().toPromise()).response;
        this._snackBar.open(res2.response, "Ok", {
          duration: 3000,
          panelClass: ['success-class'],
        });
      }
    });
  }

  async openFolder(item: Folder){
    this.folder = (await this._folderService.openFolder(item.name).toPromise()).response;
    this.paths.push(item.name);
  }

  async openFile(item: File){
    let info = (await this._fileService.getFile(item.name).toPromise()).response;
    this._openDialog.open(OpenFileComponent, {width: '1000px', data: info});
    //console.log((await this._fileService.getFile(item.name).toPromise()));
  }

  openOnMouseOver() {
    this.contextMenu.openMenu();
  }

  addFolder(){
    let done = this._openDialog.open(CreateFolderComponent, {width: '1000px'}).afterClosed();
    done.subscribe(async (res)=>{
      let res2 = (await this._folderService.createFolder(res.name).toPromise());
      if(res2.error){
        this._snackBar.open(res2.response, "Ok", {
          duration: 3000,
          panelClass: ['error-class'],
        });
      }
      else{
        this.folder = (await this._folderService.getCurrentFolder().toPromise()).response;
        this._snackBar.open(res2.response, "Ok", {
          duration: 3000,
          panelClass: ['success-class'],
        });
      }
    });
  }

  addFile(){
    let done = this._openDialog.open(CreateFileComponent, {width: '1000px'}).afterClosed();
    done.subscribe(async (res)=>{
      let res2 = (await this._fileService.createFile(res.name, res.content).toPromise());
      if(res2.error){
        this._snackBar.open(res2.response, "Ok", {
          duration: 3000,
          panelClass: ['error-class'],
        });
      }
      else{
        this.folder = (await this._folderService.getCurrentFolder().toPromise()).response;
        this._snackBar.open(res2.response, "Ok", {
          duration: 3000,
          panelClass: ['success-class'],
        });
      }
    });
  }

  async openDrive(){
    await this._userService.cleanPaths().toPromise();
    this.folder = (await this._folderService.openFolder('root').toPromise()).response;
    this.paths = ['root'];
  }

  async openShared(){
    await this._userService.cleanPaths().toPromise();
    this.folder = (await this._folderService.openFolder('shared').toPromise()).response;
    this.paths = ['shared'];
  }

  async navigate(path: string, index: number){
    console.log(this.paths);
    console.log(index);
    this.folder = (await this._folderService.goToFolder(this.paths,index).toPromise()).response;
    this.paths = this.paths.slice(0,index+1);
    //this.paths = this.paths.length===0?["root"]:this.paths;
  }

}