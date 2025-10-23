import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Artist, ArtistDTO } from './models/artist.model';

@Injectable({
  providedIn: 'root',
})
export class ArtistService {
  private apiUrl = environment.apiUrl;

  constructor(private httpClient: HttpClient) {}

  getArtists(): Observable<Artist[]> {
    return this.httpClient.get<Artist[]>(`${this.apiUrl}/artists`);
  }

  createArtist(artist: ArtistDTO): Observable<void> {
    return this.httpClient.post<void>(`${this.apiUrl}/artists`, artist);
  }

  updateArtist(id: string, artist: ArtistDTO): Observable<void> {
    return this.httpClient.put<void>(`${this.apiUrl}/artists/${id}`, artist);
  }

  deleteArtist(id: string): Observable<void> {
    return this.httpClient.delete<void>(`${this.apiUrl}/artists/${id}`);
  }
}
