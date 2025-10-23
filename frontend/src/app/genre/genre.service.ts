import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';

@Injectable({
  providedIn: 'root',
})
export class GenreService {
  private apiUrl = environment.apiUrl;

  constructor(private httpClient: HttpClient) {}

  getAll(): Observable<string[]> {
    return this.httpClient.get<string[]>(`${this.apiUrl}/genres`);
  }

  createGenre(genre: string): Observable<void> {
    return this.httpClient.post<void>(`${this.apiUrl}/genres`, { genre });
  }

  updateGenre(oldGenre: string, genre: string): Observable<void> {
    return this.httpClient.put<void>(`${this.apiUrl}/genres/${oldGenre}`, { genre });
  }

  deleteGenre(genre: string): Observable<void> {
    return this.httpClient.delete<void>(`${this.apiUrl}/genres/${genre}`);
  }
}
