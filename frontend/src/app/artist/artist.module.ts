import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MaterialModule } from '../infrastructure/material/material.module';
import { ArtistListComponent } from './artist-list/artist-list.component';
import { ArtistModalComponent } from './artist-modal/artist-modal.component';

@NgModule({
  declarations: [ArtistListComponent, ArtistModalComponent],
  imports: [CommonModule, FormsModule, MaterialModule],
  exports: [ArtistListComponent],
})
export class ArtistModule {}
