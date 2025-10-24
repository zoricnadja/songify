import { Component, OnInit } from '@angular/core';
import { Album } from '../../album/models/album.model';
import { Artist } from '../../artist/models/artist.model';
import { Track } from '../../track/models/track.model';
import { GenreService } from '../../genre/genre.service';
import { AlbumService } from '../../album/album.service';
import { ArtistService } from '../../artist/artist.service';
import { TrackService } from '../../track/track.service';

@Component({
  selector: 'app-discover',
  standalone: false,
  templateUrl: './discover.component.html',
  styleUrl: './discover.component.scss',
})
export class DiscoverComponent implements OnInit {
  genres: string[] = [];
  selectedGenre: string | null = null;
  albums: Album[] = [];
  artists: Artist[] = [];
  selectedAlbum: Album | null = null;
  selectedArtist: Artist | null = null;
  tracks: Track[] = [];
  trackReactions: Record<string, 'like' | 'dislike' | 'love' | null> = {};

  constructor(
    private genreService: GenreService,
    private albumService: AlbumService,
    private artistService: ArtistService,
    private trackService: TrackService
  ) {}

  ngOnInit() {
    this.genreService.getAll().subscribe((genres) => (this.genres = genres));
  }

  onGenreSelect(genre: string) {
    this.selectedGenre = genre;
    this.selectedAlbum = null;
    this.selectedArtist = null;
    this.tracks = [];
    this.albumService.getAlbums(genre).subscribe((albums) => {
      this.albums = albums;
    });
    this.artistService.getArtists(genre).subscribe((artists) => {
      this.artists = artists;
    });
  }

  onAlbumSelect(album: Album) {
    this.selectedAlbum = album;
    this.selectedArtist = null;
    this.trackService.getTracks(null, album.id).subscribe((tracks) => {
      this.tracks = tracks.map((t) => ({
        ...t,
        id: t.id,
      }));
      this.tracks.forEach((t) => (this.trackReactions[t.id] = null));
    });
  }

  onArtistSelect(artist: Artist) {
    this.selectedArtist = artist;
    this.selectedAlbum = null;
    this.trackService.getTracks(artist.id).subscribe((tracks) => {
      this.tracks = tracks.map((t) => ({
        ...t,
        id: t.id,
      }));
      this.tracks.forEach((t) => (this.trackReactions[t.id] = null));
    });
  }

  onLike(track: Track) {
    const newReaction = this.trackReactions[track.id] === 'like' ? null : 'like';
    this.trackReactions[track.id] = newReaction;

    const score = newReaction === 'like' ? 2 : 0;
    this.trackService.rateTrack(track.id, score).subscribe({
      next: () => console.log(`Track ${track.title} rated as Like`),
      error: (err) => console.error('Error rating track:', err),
    });
  }

  onDislike(track: Track) {
    const newReaction = this.trackReactions[track.id] === 'dislike' ? null : 'dislike';
    this.trackReactions[track.id] = newReaction;

    const score = newReaction === 'dislike' ? 1 : 0;
    this.trackService.rateTrack(track.id, score).subscribe({
      next: () => console.log(`Track ${track.title} rated as Dislike`),
      error: (err) => console.error('Error rating track:', err),
    });
  }

  onLove(track: Track) {
    const newReaction = this.trackReactions[track.id] === 'love' ? null : 'love';
    this.trackReactions[track.id] = newReaction;

    const score = newReaction === 'love' ? 3 : 0;
    this.trackService.rateTrack(track.id, score).subscribe({
      next: () => console.log(`Track ${track.title} rated as Love`),
      error: (err) => console.error('Error rating track:', err),
    });
  }
}
