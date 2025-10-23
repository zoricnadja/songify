import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SubscriptionsComponent } from './subscriptions/subscriptions.component';
import { MaterialModule } from '../infrastructure/material/material.module';
import { CreateSubscriptionComponent } from './create-subscription/create-subscription.component';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [SubscriptionsComponent, CreateSubscriptionComponent],
  imports: [CommonModule, MaterialModule, ReactiveFormsModule],
})
export class SubscriptionModule {}
