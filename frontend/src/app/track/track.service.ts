import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Track, TrackDTO } from './models/track.model';

@Injectable({
  providedIn: 'root',
})
export class TrackService {
  private apiUrl = environment.apiUrl;
  constructor(private httpClient: HttpClient) {}

  getTracks(artistId: string | null = null, albumId: string | null = null): Observable<Track[]> {
    let params = new HttpParams();
    if (artistId) {
      params = params.set('artist_id', artistId);
    }
    if (albumId) {
      params = params.set('album_id', albumId);
    }

    return this.httpClient.get<Track[]>(`${this.apiUrl}/tracks`, { params });
  }

  createTrack(track: TrackDTO): Observable<void> {
    return this.httpClient.post<void>(`${this.apiUrl}/tracks`, track);
  }

  updateTrack(id: string, track: any): Observable<any> {
    return this.httpClient.put<any>(`${this.apiUrl}/${id}`, track);
  }

  deleteTrack(id: string): Observable<void> {
    return this.httpClient.delete<void>(`${this.apiUrl}/tracks/${id}`);
  }

  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.httpClient.post<any>(`${this.apiUrl}/upload`, formData);
  }

  getPresignedUrl(fileName: string, fileType: string): Observable<{ url: string; key: string }> {
    return this.httpClient.post<{ url: string; key: string }>(`${this.apiUrl}/s3/presign-upload`, {
      fileName,
      fileType,
    });
  }

  getTrackScore(trackId: string): Observable<any> {
    return this.httpClient.get(`${this.apiUrl}/tracks/${trackId}/score`);
  }

  rateTrack(trackId: string, score: number): Observable<any> {
    return this.httpClient.post(`${this.apiUrl}/tracks/${trackId}/score`, { score });
  }
}
