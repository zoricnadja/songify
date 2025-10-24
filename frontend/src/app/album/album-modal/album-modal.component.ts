import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ArtistService } from '../../artist/artist.service';
import { GenreService } from '../../genre/genre.service';
import { Artist } from '../../artist/models/artist.model';
import { Album, AlbumDTO } from '../models/album.model';
import { TrackDTO } from '../../track/models/track.model';
import { TrackService } from '../../track/track.service';

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
  tracks: any[] = [];
  tracksToAdd: TrackDTO[] = [];

  constructor(
    public dialogRef: MatDialogRef<AlbumModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { album: Album },
    private artistService: ArtistService,
    private genreService: GenreService,
    private trackService: TrackService
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

  addTrack() {
    this.tracks.push({
      title: '',
      artistIds: [],
      genres: [],
      imageFile: null,
      imagePreview: null,
      trackFile: null,
    });
  }

  removeTrack(index: number) {
    this.tracks.splice(index, 1);
  }

  onTrackImageChange(event: any, track: any) {
    const file = event.target.files[0];
    if (file) {
      track.imageFile = file;
      const reader = new FileReader();
      reader.onload = (e) => (track.imagePreview = reader.result as string);
      reader.readAsDataURL(file);
    }
  }

  onTrackFileChange(event: any, track: any) {
    const file = event.target.files[0];
    if (file) {
      track.trackFile = file;
      track.file = {
        name: file.name,
        type: file.type,
        size: file.size,
        createdAt: file.lastModified || new Date(),
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
    return url.split('?')[0];
  }

  async onSave() {
    if (!this.title.trim() || !this.selectedArtistIds || !this.selectedGenres) return;
    const album: AlbumDTO = {
      title: this.title,
      artistIds: this.selectedArtistIds,
      genres: this.selectedGenres,
    };

    for (const track of this.tracks) {
      let imageKey = null;
      let trackKey = null;
      if (track.imageFile) {
        const presignedImage = await this.trackService
          .getPresignedUrl(track.imageFile.name, track.imageFile.type)
          .toPromise();
        imageKey = presignedImage?.key;
        await this.uploadToPresignedUrl(presignedImage!.url, track.imageFile);
      }
      if (track.trackFile) {
        const presignedTrack = await this.trackService
          .getPresignedUrl(track.trackFile.name, track.trackFile.type)
          .toPromise();
        trackKey = presignedTrack?.key;
        await this.uploadToPresignedUrl(presignedTrack!.url, track.trackFile);
      }

      const trackToAdd: TrackDTO = {
        title: track.title,
        albumId: undefined, // Will be set after album creation
        artistIds: track.artistIds,
        genres: track.genres,
        file: track.file,
        imageKey: imageKey || undefined,
        trackKey: trackKey || undefined,
      };

      this.tracksToAdd.push(trackToAdd);
    }
    this.dialogRef.close({ album, tracks: this.tracksToAdd });
  }
}
