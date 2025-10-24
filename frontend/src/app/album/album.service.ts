import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Album, AlbumDTO } from './models/album.model';

@Injectable({
  providedIn: 'root',
})
export class AlbumService {
  private apiUrl = environment.apiUrl;

  constructor(private httpClient: HttpClient) {}

  getAlbums(genre: string | null = null): Observable<Album[]> {
    let params = new HttpParams();
    if (genre) {
      params = params.set('genre', genre);
    }
    return this.httpClient.get<Album[]>(`${this.apiUrl}/albums`, { params });
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
