import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { GenreService } from '../../genre/genre.service';

@Component({
  selector: 'app-artist-modal',
  standalone: false,
  templateUrl: './artist-modal.component.html',
  styleUrl: './artist-modal.component.scss',
})
export class ArtistModalComponent implements OnInit {
  name = '';
  biography = '';
  selectedGenres: string[] = [];
  genres: string[] = [];

  constructor(
    public dialogRef: MatDialogRef<ArtistModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { name: string; biography: string; genres: string[] },
    private genreService: GenreService
  ) {
    this.name = data?.name || '';
    this.biography = data?.biography || '';
    this.selectedGenres = data?.genres || [];
  }

  ngOnInit() {
    this.genreService.getAll().subscribe((genres) => {
      this.genres = genres;
    });
  }

  onSave() {
    if (this.name.trim()) {
      this.dialogRef.close({
        name: this.name,
        biography: this.biography,
        genres: this.selectedGenres,
      });
    }
  }
}
