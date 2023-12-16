export class TabEditor{
    id: number;
    label: string;
    code: string = "";
    console: string = "";
    isActive: boolean = false;

    constructor(id: number, label: string, isActive: boolean = false){
        this.id = id;
        this.label = label;
        this.isActive = isActive;
    }
}