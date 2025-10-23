import { Component, OnInit } from '@angular/core';
import { GenreService } from '../genre.service';
import { MatDialog } from '@angular/material/dialog';
import { GenreModalComponent } from '../genre-modal/genre-modal.component';

@Component({
  selector: 'app-genre-list',
  standalone: false,
  templateUrl: './genre-list.component.html',
  styleUrl: './genre-list.component.scss',
})
export class GenreListComponent implements OnInit {
  genres: string[] = [];

  constructor(
    private genreService: GenreService,
    private dialog: MatDialog
  ) {}

  ngOnInit() {
    this.loadGenres();
  }

  loadGenres() {
    this.genreService.getAll().subscribe(
      (res) => {
        this.genres = res;
      },
      (error) => alert(error.error.message)
    );
  }

  openCreateModal() {
    this.dialog
      .open(GenreModalComponent, {
        width: '600px',
        data: { name: '' },
      })
      .afterClosed()
      .subscribe((result) => {
        if (result) {
          this.genreService.createGenre(result).subscribe(
            () => this.loadGenres(),
            (error) => alert(error.error.message)
          );
        }
      });
  }

  openEditModal(genre: string) {
    this.dialog
      .open(GenreModalComponent, {
        width: '400px',
        data: { genre },
      })
      .afterClosed()
      .subscribe((result) => {
        if (result) {
          this.genreService.updateGenre(genre, result).subscribe(
            () => this.loadGenres(),
            (error) => alert(error.error.message)
          );
        }
      });
  }

  deleteGenre(genre: string) {
    if (confirm('Are you sure you want to delete this genre?')) {
      this.genreService.deleteGenre(genre).subscribe(
        () => this.loadGenres(),
        (error) => alert(error.error.message)
      );
    }
  }
}
