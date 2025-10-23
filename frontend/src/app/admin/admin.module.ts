import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';
import { GenreModule } from '../genre/genre.module';

@NgModule({
  declarations: [AdminPanelComponent],
  imports: [CommonModule, GenreModule],
})
export class AdminModule {}
