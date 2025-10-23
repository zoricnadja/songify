import { Component, OnInit } from '@angular/core';
import { CreateSubscription, Subscription } from '../subscription.model';
import { SubscriptionService } from '../subscription.service';
import { MatDialog } from '@angular/material/dialog';
import { CreateSubscriptionComponent } from '../create-subscription/create-subscription.component';

@Component({
  selector: 'app-subscriptions',
  standalone: false,
  templateUrl: './subscriptions.component.html',
  styleUrls: ['./subscriptions.component.scss'],
})
export class SubscriptionsComponent implements OnInit {
  subscriptions: Subscription[] = [];
  loading = false;
  error: string | null = null;

  constructor(
    private dialog: MatDialog,
    private subscriptionService: SubscriptionService
  ) {}

  async ngOnInit(): Promise<void> {
    this.fetchSubscriptions();
  }

  fetchSubscriptions(): void {
    this.loading = true;
    this.subscriptionService.getSubscriptions().subscribe({
      next: (data) => {
        this.subscriptions = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error fetching subscriptions', err);
        this.error = 'Failed to load subscriptions';
        this.loading = false;
      },
    });
  }

  deleteSubscription(id: string): void {
    if (!confirm('Are you sure you want to delete this subscription?')) return;

    this.subscriptionService.delete(id).subscribe({
      next: () => {
        this.subscriptions = this.subscriptions.filter((s) => s.id !== id);
      },
      error: (err) => {
        console.error('Error deleting subscription', err);
        alert('Error deleting subscription');
      },
    });
  }

  openAddDialog(): void {
    const dialogRef = this.dialog.open(CreateSubscriptionComponent, { width: '400px' });

    dialogRef.afterClosed().subscribe((result: CreateSubscription | undefined) => {
      if (!result) return;

      this.subscriptionService.create(result).subscribe({
        next: () => {
          this.fetchSubscriptions();
        },
        error: (err) => {
          console.error('Error while creating subscription', err);
          alert('Error while creating subscription.');
        },
      });
    });
  }
}
