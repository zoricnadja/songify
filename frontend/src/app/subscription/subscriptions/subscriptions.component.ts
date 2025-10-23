import { Component, OnInit } from '@angular/core';
import { Subscription } from '../subscription.model';
import { SubscriptionService } from '../subscription.service';

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

  constructor(private subscriptionService: SubscriptionService) {}

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
}
