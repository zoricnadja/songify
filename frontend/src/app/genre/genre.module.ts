import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GenreListComponent } from './genre-list/genre-list.component';
import { GenreModalComponent } from './genre-modal/genre-modal.component';
import { MaterialModule } from '../infrastructure/material/material.module';

@NgModule({
  declarations: [GenreListComponent, GenreModalComponent],
  imports: [CommonModule, FormsModule, MaterialModule],
  exports: [GenreListComponent],
})
export class GenreModule {}
