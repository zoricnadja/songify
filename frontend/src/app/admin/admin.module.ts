import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';
import { GenreModule } from '../genre/genre.module';
import { ArtistModule } from '../artist/artist.module';

@NgModule({
  declarations: [AdminPanelComponent],
  imports: [CommonModule, GenreModule, ArtistModule],
})
export class AdminModule {}
