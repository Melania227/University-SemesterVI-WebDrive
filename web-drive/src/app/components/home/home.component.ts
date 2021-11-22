import { Component, OnInit, ViewChild } from '@angular/core';
import { MatMenuTrigger } from '@angular/material/menu';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  openDrive(){
    console.log("Open Drive")
  }

  openShared(){
    console.log("Open Shared")
  }

  items = [
    {id: 1, name: 'Item 1', type: 'file'},
    {id: 2, name: 'Item 2', type: 'file'},
    {id: 3, name: 'Item 3', type: 'file'},
    {id: 4, name: 'Item 4', type: 'folder'},
    {id: 5, name: 'Item 5', type: 'file'},
    {id: 6, name: 'Item 6', type: 'file'},
    {id: 7, name: 'Item 7', type: 'folder'},
    {id: 8, name: 'Item 8', type: 'file'},
    {id: 9, name: 'Item 9', type: 'folder'}
  ];

  @ViewChild(MatMenuTrigger) contextMenu!: MatMenuTrigger;

  contextMenuPosition = { x: '0px', y: '0px' };

  onContextMenu(event: MouseEvent, item: Item) {
    event.preventDefault();
    this.contextMenuPosition.x = event.clientX + 'px';
    this.contextMenuPosition.y = event.clientY + 'px';
    this.contextMenu.menuData = { 'item': item };
    this.contextMenu.menu.focusFirstItem('mouse');
    this.contextMenu.openMenu();
  }

  onContextMenuOpen(item: Item) {
    alert(`Open ${item.name}`);
  }

  onContextMenuEdit(item: Item) {
    alert(`Edit ${item.name}`);
  }

  onContextMenuCopy(item: Item) {
    alert(`Copy ${item.name}`);
  }

  onContextMenuMove(item: Item) {
    alert(`Move ${item.name}`);
  }

  onContextMenuShare(item: Item){
    alert(`Share ${item.name}`);
  }

  onContextMenuAddFile(){
    alert(`Create File`);
  }

  onContextMenuAddFolder(){
    alert(`Create Folder`);
  }

  open(item: Item){
    alert(`Open ${item.name}`);
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

}

export interface Item {
  id: number;
  name: string;
  type: string;
}