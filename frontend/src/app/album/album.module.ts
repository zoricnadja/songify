import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AlbumListComponent } from './album-list/album-list.component';
import { AlbumModalComponent } from './album-modal/album-modal.component';
import { MaterialModule } from '../infrastructure/material/material.module';

@NgModule({
  declarations: [AlbumListComponent, AlbumModalComponent],
  imports: [CommonModule, FormsModule, MaterialModule],
  exports: [AlbumListComponent],
})
export class AlbumModule {}
