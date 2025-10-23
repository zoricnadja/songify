import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ArtistService } from '../../artist/artist.service';
import { GenreService } from '../../genre/genre.service';
import { Artist } from '../../artist/models/artist.model';
import { Album, AlbumDTO } from '../models/album.model';

@Component({
  selector: 'app-album-modal',
  standalone: false,
  templateUrl: './album-modal.component.html',
  styleUrl: './album-modal.component.scss',
})
export class AlbumModalComponent implements OnInit {
  artists: Artist[] = [];
  genres: string[] = [];

  title = '';
  selectedArtistIds: string[] = [];
  selectedGenres: string[] = [];

  constructor(
    public dialogRef: MatDialogRef<AlbumModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { album: Album },
    private artistService: ArtistService,
    private genreService: GenreService
  ) {
    this.title = data?.album.title || '';
    this.selectedArtistIds = data?.album.artists.map((artist) => artist.id) || '';
    this.selectedGenres = data?.album.genres || [];
  }

  ngOnInit() {
    this.artistService.getArtists().subscribe((artists) => {
      this.artists = artists;
    });
    this.genreService.getAll().subscribe((genres) => {
      this.genres = genres;
    });
  }

  onSave() {
    if (this.title.trim() && this.selectedArtistIds && this.selectedGenres) {
      const album: AlbumDTO = {
        title: this.title,
        artistIds: this.selectedArtistIds,
        genres: this.selectedGenres,
      };

      this.dialogRef.close(album);
    }
  }
}
