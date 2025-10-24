import { Component, OnInit } from '@angular/core';
import { AlbumService } from '../album.service';
import { MatDialog } from '@angular/material/dialog';
import { AlbumModalComponent } from '../album-modal/album-modal.component';
import { Album } from '../models/album.model';
import { TrackService } from '../../track/track.service';

@Component({
  selector: 'app-album-list',
  standalone: false,
  templateUrl: './album-list.component.html',
  styleUrl: './album-list.component.scss',
})
export class AlbumListComponent implements OnInit {
  albums: Album[] = [];

  constructor(
    private albumService: AlbumService,
    private trackService: TrackService,
    private dialog: MatDialog
  ) {}

  ngOnInit() {
    this.loadAlbums();
  }

  loadAlbums() {
    this.albumService.getAlbums().subscribe((albums) => {
      this.albums = albums;
    });
  }

  openCreateModal() {
    this.dialog
      .open(AlbumModalComponent, {
        width: '500px',
      })
      .afterClosed()
      .subscribe((result) => {
        if (result) {
          this.albumService.createAlbum(result.album).subscribe(
            (response) => {
              for (const track of result.tracks) {
                track.albumId = response.album_id;
                this.trackService.createTrack(track).subscribe();
              }
              this.loadAlbums();
            },
            (error) => alert(error.error.message)
          );
        }
      });
  }

  openEditModal(album: Album) {
    this.dialog
      .open(AlbumModalComponent, {
        width: '500px',
        data: { album },
      })
      .afterClosed()
      .subscribe((result) => {
        if (result) {
          this.albumService.updateAlbum(album.id, result.album).subscribe(
            () => this.loadAlbums(),
            (error) => alert(error.error.message)
          );
        }
      });
  }

  deleteAlbum(album: Album) {
    if (confirm('Are you sure you want to delete this album?')) {
      this.albumService.deleteAlbum(album.id).subscribe(
        () => this.loadAlbums(),
        (error) => alert(error.error.message)
      );
    }
  }
}
