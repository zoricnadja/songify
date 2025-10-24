import { Component } from '@angular/core';
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
export class DiscoverComponent {
  genres: string[] = [];
  selectedGenre: string | null = null;
  albums: Album[] = [];
  artists: Artist[] = [];
  selectedAlbum: Album | null = null;
  selectedArtist: Artist | null = null;
  tracks: Track[] = [];

  constructor(
    private genreService: GenreService,
    private albumService: AlbumService,
    private artistService: ArtistService,
    private trackService: TrackService
  ) {}

  ngOnInit() {
    this.genreService.getAll().subscribe(genres => this.genres = genres);
  }

  onGenreSelect(genre: string) {
    this.selectedGenre = genre;
    this.selectedAlbum = null;
    this.selectedArtist = null;
    this.tracks = [];
    this.albumService.getAlbums(genre).subscribe(albums => {
      this.albums = albums;
    });
    this.artistService.getArtists(genre).subscribe(artists => {
      this.artists = artists;
    });
  }

  onAlbumSelect(album: Album) {
    this.selectedAlbum = album;
    this.selectedArtist = null;
    this.trackService.getTracks(null, album.id).subscribe(tracks => {
      this.tracks = tracks;
    });
  }

  onArtistSelect(artist: Artist) {
    this.selectedArtist = artist;
    this.selectedAlbum = null;
    this.trackService.getTracks(artist.id).subscribe(tracks => {
      this.tracks = tracks;
    });
  }
}
