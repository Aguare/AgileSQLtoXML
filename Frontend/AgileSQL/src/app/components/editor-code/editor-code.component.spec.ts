import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditorCodeComponent } from './editor-code.component';

describe('EditorCodeComponent', () => {
  let component: EditorCodeComponent;
  let fixture: ComponentFixture<EditorCodeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EditorCodeComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditorCodeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
