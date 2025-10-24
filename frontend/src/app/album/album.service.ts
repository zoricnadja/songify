import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Album, AlbumDTO } from './models/album.model';

@Injectable({
  providedIn: 'root',
})
export class AlbumService {
  private apiUrl = environment.apiUrl;

  constructor(private httpClient: HttpClient) {}

  getAlbums(): Observable<Album[]> {
    return this.httpClient.get<Album[]>(`${this.apiUrl}/albums`);
  }
  createAlbum(album: AlbumDTO): Observable<{ album_id: string }> {
    return this.httpClient.post<{ album_id: string }>(`${this.apiUrl}/albums`, album);
  }
  updateAlbum(id: string, album: AlbumDTO): Observable<void> {
    return this.httpClient.put<void>(`${this.apiUrl}/albums/${id}`, album);
  }
  deleteAlbum(id: string): Observable<void> {
    return this.httpClient.delete<void>(`${this.apiUrl}/albums/${id}`);
  }
}
