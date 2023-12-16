import { Component, Input } from '@angular/core';
import { DataBase } from '../../models/DataBase';
import { Table } from '../../models/Table';

@Component({
  selector: 'app-tree-view',
  templateUrl: './tree-view.component.html',
  styleUrl: './tree-view.component.scss'
})
export class TreeViewComponent {
  @Input() dataBases: Array<DataBase> = [];

  selectBD(id: number) {
    let db = this.dataBases.find(db => db.id === id);
    if (db) {
      db.isActive = !db.isActive;
    }
  }

  showTablesBD(id: number) {
    let db = this.dataBases.find(db => db.id === id);
    if (db) {
      db.showTables = !db.showTables;
    }
  }

  showFunctionsBD(id: number) {
    let db = this.dataBases.find(db => db.id === id);
    if (db) {
      db.showFunctions = !db.showFunctions;
    }
  }

  showProceduresBD(id: number) {
    let db = this.dataBases.find(db => db.id === id);
    if (db) {
      db.showProcedures = !db.showProcedures;
    }
  }
}
