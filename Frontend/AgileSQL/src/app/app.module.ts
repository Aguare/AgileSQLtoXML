import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CodemirrorModule } from '@ctrl/ngx-codemirror'; 
import { HomeComponent } from './components/home/home.component';
import { EditorCodeComponent } from './components/editor-code/editor-code.component';
import { AngularFontAwesomeModule } from 'angular-font-awesome';
import { TreeViewComponent } from './components/tree-view/tree-view.component';
import { DataTableComponent } from './components/data-table/data-table.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    EditorCodeComponent,
    TreeViewComponent,
    DataTableComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    CodemirrorModule,
    ReactiveFormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
