export interface CreateSubscription {
  targetType: string;
  targetId: string;
}

export interface Subscription {
  targetType: string;
  targetId: string;
  targetName: string;
  createdAt: string;
  id: string;
}
