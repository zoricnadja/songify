import { Component, OnInit } from '@angular/core';
import { ArtistService } from '../artist.service';
import { MatDialog } from '@angular/material/dialog';
import { ArtistModalComponent } from '../artist-modal/artist-modal.component';
import { Artist } from '../models/artist.model';

@Component({
  selector: 'app-artist-list',
  standalone: false,
  templateUrl: './artist-list.component.html',
  styleUrl: './artist-list.component.scss',
})
export class ArtistListComponent implements OnInit {
  artists: Artist[] = [];

  constructor(
    private artistService: ArtistService,
    private dialog: MatDialog
  ) {}

  ngOnInit() {
    this.loadArtists();
  }

  loadArtists() {
    this.artistService.getArtists().subscribe((artists) => {
      this.artists = artists;
    });
  }

  openCreateModal() {
    this.dialog
      .open(ArtistModalComponent, {
        width: '500px',
        data: { name: '', biography: '', genres: [] },
      })
      .afterClosed()
      .subscribe((result) => {
        if (result) {
          this.artistService.createArtist(result).subscribe(
            () => this.loadArtists(),
            (error) => alert(error.error.message)
          );
        }
      });
  }

  openEditModal(artist: Artist) {
    this.dialog
      .open(ArtistModalComponent, {
        width: '500px',
        data: { ...artist },
      })
      .afterClosed()
      .subscribe((result) => {
        if (result) {
          this.artistService.updateArtist(artist.id, result).subscribe(
            () => this.loadArtists(),
            (error) => alert(error.error.message)
          );
        }
      });
  }

  deleteArtist(artist: Artist) {
    if (confirm('Are you sure you want to delete this artist?')) {
      this.artistService.deleteArtist(artist.id).subscribe(
        () => this.loadArtists(),
        (error) => alert(error.error.message)
      );
    }
  }
}
