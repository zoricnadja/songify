import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { Genre } from './models/genre.model';

@Injectable({
  providedIn: 'root',
})
export class GenreService {
  private apiUrl = environment.apiUrl;

  constructor(private httpClient: HttpClient) {}

  getAll(): Observable<Genre[]> {
    return this.httpClient.get<Genre[]>(`${this.apiUrl}/genres`);
  }

  createGenre(genre: Genre): Observable<Genre> {
    return this.httpClient.post<Genre>(`${this.apiUrl}/genres`, genre);
  }

  updateGenre(name: string, genre: Genre): Observable<Genre> {
    return this.httpClient.put<Genre>(`${this.apiUrl}/genres/${name}`, genre);
  }

  deleteGenre(name: string): Observable<void> {
    return this.httpClient.delete<void>(`${this.apiUrl}/genres/${name}`);
  }
}
