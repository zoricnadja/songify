import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-genre-modal',
  standalone: false,
  templateUrl: './genre-modal.component.html',
  styleUrl: './genre-modal.component.scss',
})
export class GenreModalComponent {
  genre = '';

  constructor(
    public dialogRef: MatDialogRef<GenreModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { genre: string }
  ) {
    this.genre = data?.genre || '';
  }

  onSave() {
    if (this.genre.trim()) {
      this.dialogRef.close(this.genre);
    }
  }
}
