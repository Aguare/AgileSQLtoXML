import { Component, Input } from '@angular/core';
import 'codemirror/mode/sql/sql';
import 'codemirror/theme/dracula.css';

@Component({
  selector: 'app-editor-code',
  templateUrl: './editor-code.component.html',
  styleUrl: './editor-code.component.scss'
})
export class EditorCodeComponent {
  @Input() code: any = 'SELECT * FROM table';
}
