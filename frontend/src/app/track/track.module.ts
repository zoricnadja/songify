import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MaterialModule } from '../infrastructure/material/material.module';
import { TrackListComponent } from './track-list/track-list.component';
import { TrackModalComponent } from './track-modal/track-modal.component';

@NgModule({
  declarations: [TrackListComponent, TrackModalComponent],
  imports: [CommonModule, FormsModule, MaterialModule],
  exports: [TrackListComponent],
})
export class TrackModule {}
