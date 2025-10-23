import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { GenreService } from '../../genre/genre.service';
import { ArtistService } from '../../artist/artist.service';
import { AlbumService } from '../../album/album.service';
import { TrackService } from '../track.service';
import { TrackDTO } from '../models/track.model';
import { Album } from '../../album/models/album.model';
import { Artist } from '../../artist/models/artist.model';

@Component({
  selector: 'app-track-modal',
  standalone: false,
  templateUrl: './track-modal.component.html',
  styleUrl: './track-modal.component.scss',
})
export class TrackModalComponent implements OnInit {
  title = '';
  selectedGenres: string[] = [];
  selectedArtistIds: string[] = [];
  selectedAlbumId = '';
  imageFile: File | null = null;
  trackFile: File | null = null;
  imagePreview: string | null = null;
  albums: Album[] = [];
  genres: string[] = [];
  artists: Artist[] = [];
  fileInfo: {
    name: string;
    type: string;
    size: number;
    createdAt: Date;
    updatedAt: Date;
  } = {
    name: '',
    type: '',
    size: 0,
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  constructor(
    public dialogRef: MatDialogRef<TrackModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private genreService: GenreService,
    private artistService: ArtistService,
    private albumService: AlbumService,
    private trackService: TrackService
  ) {
    this.title = data?.title || '';
    this.selectedGenres = data?.genres || [];
    this.selectedArtistIds = data?.artists.map((artist: Artist) => artist.id) || [];
    this.selectedAlbumId = data?.album.id || '';
    this.fileInfo = data?.fileInfo || {};
  }

  ngOnInit() {
    this.genreService.getAll().subscribe((genres) => (this.genres = genres));
    this.artistService.getArtists().subscribe((artists) => (this.artists = artists));
    this.albumService.getAlbums().subscribe((albums) => (this.albums = albums));
  }

  onImageChange(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.imageFile = file;
      const reader = new FileReader();
      reader.onload = (e) => (this.imagePreview = reader.result as string);
      reader.readAsDataURL(file);
    }
  }

  onTrackFileChange(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.trackFile = file;
      this.fileInfo = {
        name: file.name,
        type: file.type,
        size: file.size,
        createdAt: new Date(file.lastModified), // || new Date(),
        updatedAt: new Date(),
      };
    }
  }

  async uploadToPresignedUrl(url: string, file: File) {
    await fetch(url, {
      method: 'PUT',
      body: file,
      headers: {
        'Content-Type': file.type,
      },
    });
    // Remove query params for public URL
    return url.split('?')[0];
  }

  async onSave() {
    // if (!this.title.trim() || !this.trackFile) return;
    // let imageUrl = null;
    // let trackUrl = null;
    let imageKey = null;
    let trackKey = null;

    if (this.imageFile) {
      const t = await this.trackService
        .getPresignedUrl(this.imageFile.name, this.imageFile.type)
        .toPromise();

      await this.uploadToPresignedUrl(t!.url, this.imageFile);

      imageKey = t?.key;
    }

    if (this.trackFile) {
      const t = await this.trackService
        .getPresignedUrl(this.trackFile.name, this.trackFile.type)
        .toPromise();

      await this.uploadToPresignedUrl(t!.url, this.trackFile);

      trackKey = t?.key;
    }

    const track: TrackDTO = {
      title: this.title,
      artistIds: this.selectedArtistIds,
      genres: this.selectedGenres,
      albumId: this.selectedAlbumId || undefined,
      file: this.fileInfo,
      imageKey: imageKey || undefined,
      trackKey: trackKey || undefined,
    };

    this.dialogRef.close(track);
  }
}
