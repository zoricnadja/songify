import { Artist } from '../../artist/models/artist.model';

export interface Album {
  id: string;
  title: string;
  artists: Artist[];
  genres: string[];
}

export interface AlbumDTO {
  title: string;
  artistIds: string[];
  genres: string[];
}
