import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DiscoverComponent } from './discover/discover.component';
import { MaterialModule } from '../infrastructure/material/material.module';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [DiscoverComponent],
  imports: [CommonModule, MaterialModule, FormsModule],
})
export class DiscoverModule {}
