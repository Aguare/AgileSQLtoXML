import { Component } from '@angular/core';
import { TabEditor } from '../../models/TabEditor';
import { DataBase } from '../../models/DataBase';
import { Table } from '../../models/Table';
import Swal from 'sweetalert2';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  code: any = 'SELECT * FROM table';
  console: any = 'Console messages';
  tabs: Array<TabEditor> = [
    new TabEditor(1, "Tab 1", true),
    new TabEditor(2, "Tab 2"),
    new TabEditor(3, "Tab 3"),
  ];

  tables_ex: Table[] = [
    {
      id: 1,
      name: "Table 1",
      columns: ["Column 1", "Column 2", "Column 3"]
    },
    {
      id: 2,
      name: "Table 2",
      columns: ["Column 1", "Column 2", "Column 3"]
    },
    {
      id: 3,
      name: "Table 3",
      columns: ["Column 1", "Column 2", "Column 3"]
    },
  ];

  functions_ex: any[] = [
    "Function 1",
    "Function 2",
    "Function 3",
  ];

  procedures_ex: any[] = [
    "Procedure 1",
    "Procedure 2",
    "Procedure 3",
  ];

  dataBases: Array<DataBase> = [
    new DataBase(1, "DataBase 1", this.tables_ex, this.functions_ex, this.procedures_ex),
    new DataBase(2, "DataBase 2", this.tables_ex, undefined, this.functions_ex),
    new DataBase(3, "DataBase 3", this.tables_ex, this.functions_ex, this.procedures_ex),
  ];

  selectTab(tab: any) {
    this.tabs.forEach((tab: any) => tab.isActive = false);
    tab.isActive = true;
    this.code = tab.code;
  }

  closeAllTabs() {
    Swal.fire({
      title: '¿Está seguro?',
      text: "Se cerrarán todas las pestañas abiertas",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33'
    }).then((result: any) => {
      if (result.isConfirmed) {
        this.tabs = [];
        this.addTab();
      }
    })
  }

  closeTab(tab: any) {
    if (tab.code == ""){
      this.closeTabDefinitive(tab);
      return;
    }

    Swal.fire({
      title: '¿Está seguro?',
      text: "Se cerrará la pestaña actual",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33'
    }).then((result: any) => {
      if (result.isConfirmed) {
        this.closeTabDefinitive(tab);
      }
    })
  }

  private closeTabDefinitive(tab: any) {
    let index = this.tabs.indexOf(tab);
    this.tabs.splice(index, 1);
    if (this.tabs.length == 0) {
      this.addTab();
    } else {
      this.selectTab(this.tabs[this.tabs.length - 1]);
    }
  }

  addTab(content?: string) {
    let newTab = new TabEditor(this.tabs.length + 1, "Tab " + (this.tabs.length + 1));
    this.tabs.push(newTab);
    this.selectTab(newTab);
    if (content) {
      newTab.code = content;
    }
  }

  onFileSelected(event: any): void {
    const file: File = event.target.files[0];

    if (file) {
      const allowedExtensions = ['.sql', '.txt'];
      const isValidExtension = allowedExtensions.some(ext => file.name.toLowerCase().endsWith(ext));

      if (isValidExtension) {
        this.readFile(file);
      } else {
        Swal.fire({
          title: 'Error',
          text: 'El archivo seleccionado no tiene una extensión válida (sql o txt).',
          icon: 'error',
          confirmButtonText: 'Aceptar'
        });
      }
    }
  }

  private readFile(file: File): void {
    const reader = new FileReader();

    reader.onload = (e: any) => {
      const sqlContent: string = e.target.result;
      this.addTab(sqlContent);
    };

    reader.readAsText(file);
  }

  saveTabToSQL(): void {
    const tabSelected = this.tabs.find(tab => tab.isActive);

    if (tabSelected) {
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(new Blob([tabSelected.code], { type: 'text/plain; charset=utf-8' }));
      link.download = tabSelected.label + '.sql';

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(link.href);
      Swal.fire({
        title: 'Guardado',
        text: 'El archivo se ha guardado correctamente.',
        icon: 'success',
        confirmButtonText: 'Aceptar'
      });
    }
  }
  
}
