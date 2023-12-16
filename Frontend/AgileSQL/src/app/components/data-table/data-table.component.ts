import { Component } from '@angular/core';

@Component({
  selector: 'app-data-table',
  templateUrl: './data-table.component.html',
  styleUrl: './data-table.component.scss'
})
export class DataTableComponent {
  nums: string[] = ['1', '2', '3', '4', '5', '6', '7',
    '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'];

  columns: string[] = this.nums;
  data: string[][] = [
    this.nums,
    this.nums,
    this.nums,
    this.nums,
    this.nums,
    this.nums,
    this.nums,
    this.nums,
    this.nums,
    this.nums,
    this.nums,
    this.nums,
  ];

}
