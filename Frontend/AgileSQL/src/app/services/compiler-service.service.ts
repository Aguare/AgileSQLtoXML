import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CompilerServiceService {

  URL = 'http://127.0.0.1:5000/api/';

  constructor() { }

  compile(code: string) {
    return fetch(this.URL + 'compile', {
      method: 'POST',
      body: JSON.stringify({
        codigo: code
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
}
