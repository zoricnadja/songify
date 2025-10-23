import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';
import { HttpClient } from '@angular/common/http';
import { Subscription } from './subscription.model';
import { CreateSubscription } from './subscription.model';

@Injectable({
  providedIn: 'root',
})
export class SubscriptionService {
  constructor(private httpClient: HttpClient) {}

  getSubscriptions(): Observable<Subscription[]> {
    return this.httpClient.get<Subscription[]>(`${environment.apiUrl}/subscriptions`);
  }

  create(subscription: CreateSubscription): Observable<Subscription> {
    console.log(subscription);
    return this.httpClient.post<Subscription>(`${environment.apiUrl}/subscriptions`, subscription);
  }

  delete(id: string): Observable<any> {
    return this.httpClient.delete(`${environment.apiUrl}/subscriptions/` + id);
  }
}
