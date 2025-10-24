import { Album } from '../../album/models/album.model';
import { Artist } from '../../artist/models/artist.model';

export interface Track {
  id: string;
  title: string;
  album?: Album;
  artists: Artist[];
  genres: string[];
  file: FileInfo;
  imageUrl: string;
  trackUrl: string;
}

export interface TrackDTO {
  title: string;
  albumId?: string;
  artistIds: string[];
  genres: string[];
  file: FileInfo;
  imageKey?: string;
  trackKey?: string;
}

export interface FileInfo {
  name: string;
  type: string;
  size: number;
  createdAt: Date;
  updatedAt: Date;
}
