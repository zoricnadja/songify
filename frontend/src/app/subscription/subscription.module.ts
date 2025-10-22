import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SubscriptionsComponent } from './subscriptions/subscriptions.component';
import { MaterialModule } from '../infrastructure/material/material.module';

@NgModule({
  declarations: [SubscriptionsComponent],
  imports: [CommonModule, MaterialModule],
})
export class SubscriptionModule {}
