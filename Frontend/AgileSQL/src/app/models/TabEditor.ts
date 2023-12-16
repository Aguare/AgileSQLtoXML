export class TabEditor{
    id: number;
    label: string;
    code: string = "CREATE DATABASE patitoJuan; USE patitoJuan;";
    console: string = "";
    isActive: boolean = false;

    constructor(id: number, label: string, isActive: boolean = false){
        this.id = id;
        this.label = label;
        this.isActive = isActive;
    }
}