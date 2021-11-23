import { Component, OnInit, ViewChild } from '@angular/core';
import { MatMenuTrigger } from '@angular/material/menu';
import { Folder } from 'src/app/models/folder.model';
import { FilesService } from 'src/app/services/files.service';
import { FolderService } from 'src/app/services/folders.service';

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
    private readonly _fileService: FilesService
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

  onContextMenuOpen(item: (File|Folder)) {
    alert(`Open ${item.name}`);
  }

  onContextMenuEdit(item: (File|Folder)) {
    alert(`Edit ${item.name}`);
  }

  onContextMenuCopy(item: (File|Folder)) {
    alert(`Copy ${item.name}`);
  }

  onContextMenuMove(item: (File|Folder)) {
    alert(`Move ${item.name}`);
  }

  onContextMenuShare(item: (File|Folder)){
    alert(`Share ${item.name}`);
  }

  onContextMenuAddFile(){
    alert(`Create File`);
  }

  onContextMenuAddFolder(){
    alert(`Create Folder`);
  }

  async open(item: (File|Folder)){
    if (item.type!=="file"){
      this.folder = (await this._folderService.openFolder(item.name).toPromise()).response;
      this.paths.push(item.name);
    }
    else{
      this.openFile(item);
    }
  }

  async openFile(item: (File|Folder)){
    alert((await this._fileService.getFile(item.name).toPromise()).response);
    //console.log((await this._fileService.getFile(item.name).toPromise()));
  }

  openOnMouseOver() {
    this.contextMenu.openMenu();
  }

  addFolder(){
    console.log("addFolder");
  }

  addFile(){
    console.log("addFile");
  }

  openDrive(){
    console.log("Open Drive")
  }

  openShared(){
    console.log("Open Shared")
  }

}