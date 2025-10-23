export interface Artist {
  id: string;
  name: string;
  biography: string;
  genres: string[];
}

export interface ArtistDTO {
  name: string;
  biography: string;
  genres: string[];
}
