import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MaterialModule } from '../infrastructure/material/material.module';
import { TrackListComponent } from './track-list/track-list.component';
import { TrackModalComponent } from './track-modal/track-modal.component';
import { TrackPlayerListComponent } from './track-player-list/track-player-list.component';

@NgModule({
  declarations: [TrackListComponent, TrackModalComponent, TrackPlayerListComponent],
  imports: [CommonModule, FormsModule, MaterialModule],
  exports: [TrackListComponent, TrackPlayerListComponent],
})
export class TrackModule {}
