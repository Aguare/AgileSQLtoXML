import { Table } from "./Table";

export class DataBase {
    id: number;
    name: string;
    tables: Array<Table> = [];
    functions?: Array<any> = [];
    procedures?: Array<any> = [];
    isActive: boolean = false;
    showTables: boolean = false;
    showFunctions: boolean = false;
    showProcedures: boolean = false;

    constructor(id: number, name: string, tables: Array<Table>, functions?: Array<any>, procedures?: Array<any>) {
        this.id = id;
        this.name = name;
        this.tables = tables;
        this.functions = functions;
        this.procedures = procedures;
    }

}