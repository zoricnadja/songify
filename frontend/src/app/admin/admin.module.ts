import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';
import { GenreModule } from '../genre/genre.module';
import { ArtistModule } from '../artist/artist.module';
import { AlbumModule } from '../album/album.module';
import { TrackModule } from '../track/track.module';

@NgModule({
  declarations: [AdminPanelComponent],
  imports: [CommonModule, GenreModule, ArtistModule, AlbumModule, TrackModule],
})
export class AdminModule {}
