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
import { FilesystemService } from 'src/app/services/filesystem.service';
import { Router } from '@angular/router';
import { File } from 'src/app/models/file.model';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  folder!: any;
  paths: string[]=[];
  fileNameToUpload!:string;
  dataUploaded!:string;

  @ViewChild(MatMenuTrigger) contextMenu!: MatMenuTrigger;

  contextMenuPosition = { x: '0px', y: '0px' };

  constructor(
    private readonly _folderService: FolderService,
    private readonly _fileService: FilesService,
    public _fileSystemService: FilesystemService,
    private readonly _userService: UserService,
    private readonly _router: Router,
    private _openDialog: MatDialog,
    private _snackBar: MatSnackBar,
  ) { }

  async ngOnInit():Promise<void> {
    (await this._userService.cleanPaths().toPromise());
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

  async onContextMenuDelete(item: (File|Folder)) {
    let info;
    if(item.type==="file"){
      info = (await this._fileService.deleteFile(item.name).toPromise());
    }
    else{
      info = (await this._folderService.deleteFolder(item.name).toPromise());
    }

    if(info.error){
      this._snackBar.open(info.response, "Ok", {
        duration: 3000,
        panelClass: ['error-class'],
      });
    }
    else{
      this.folder = (await this._folderService.getCurrentFolder().toPromise()).response;
      this._snackBar.open(info.response, "Ok", {
        duration: 3000,
        panelClass: ['success-class'],
      });
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

  async onContextMenuCopy(item: (File|Folder)) {
    (await this._fileSystemService.saveCopyInfo(item.name));
  }

  async onContextMenuMove(item: (File|Folder)) {
    (await this._fileSystemService.saveMoveInfo(item.name));
    (await this._userService.cleanPaths().toPromise());
    this.folder = (await this._folderService.openFolder('root').toPromise()).response;
    this.paths = ['root'];
  }

  async pasteHere(){
    if (this._fileSystemService.isCopying()){
      let info = (await this._fileSystemService.copy().toPromise());
      this._fileSystemService.cleanVariables();
      if(info.error){
        this._snackBar.open(info.response, "Ok", {
          duration: 3000,
          panelClass: ['error-class'],
        });
      }
      else{
        this.folder = (await this._folderService.getCurrentFolder().toPromise()).response;
        this._snackBar.open(info.response, "Ok", {
          duration: 3000,
          panelClass: ['success-class'],
        });
      }
    }
    else{
      this._snackBar.open("There's nothing on clipboard", "Ok", {
        duration: 3000,
        panelClass: ['error-class'],
      });
    }
  }

  async moveHere(){
    let info = (await this._fileSystemService.move().toPromise());
    this._fileSystemService.cleanVariables();
    if(info.error){
      this._snackBar.open(info.response, "Ok", {
        duration: 3000,
        panelClass: ['error-class'],
      });
    }
    else{
      this.folder = (await this._folderService.getCurrentFolder().toPromise()).response;
      this._snackBar.open(info.response, "Ok", {
        duration: 3000,
        panelClass: ['success-class'],
      });
    }
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
    this.folder = (await this._folderService.goToFolder(this.paths,index).toPromise()).response;
    this.paths = this.paths.slice(0,index+1);
  }


  /* DOWNLOAD */
  uploadFile(event:any) {
    let file = event.target.files[0];
    this.fileNameToUpload = file.name
    this.readFile(file).then(async (result)=>{
      await this._fileService.createFile(this.fileNameToUpload, this.dataUploaded).toPromise();
      this.fileNameToUpload="";
      this.dataUploaded="";
      this.folder = (await this._folderService.getCurrentFolder().toPromise()).response;
    })
  }

  readFile(file:Blob){
    return new Promise((resolve, reject) => {
      var fr = new FileReader();  
      fr.onload = () => {
        this.dataUploaded = fr.result as string
        resolve(fr.result as string)
      };
      fr.onerror = reject;
      fr.readAsText(file);
    });
  }

  doDownload(filename:string, text:string) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  }
  
  onContextMenuDownload(item:File){
    this.doDownload(item.name,item.data);
  }

  onContextMenuDownloadError(){
    this._snackBar.open("It's impossible to download a folder.", "Ok", {
      duration: 3000,
      panelClass: ['error-class'],
    });
  }

}