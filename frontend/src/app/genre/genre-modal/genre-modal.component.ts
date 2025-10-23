import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-genre-modal',
  standalone: false,
  templateUrl: './genre-modal.component.html',
  styleUrl: './genre-modal.component.scss',
})
export class GenreModalComponent {
  name = '';

  constructor(
    public dialogRef: MatDialogRef<GenreModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { name: string }
  ) {
    this.name = data?.name || '';
  }

  onSave() {
    if (this.name.trim()) {
      this.dialogRef.close({ name: this.name });
    }
  }
}
