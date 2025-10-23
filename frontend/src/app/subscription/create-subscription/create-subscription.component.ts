import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CreateSubscription } from '../subscription.model';

@Component({
  selector: 'app-create-subscription',
  standalone: false,
  templateUrl: './create-subscription.component.html',
  styleUrl: './create-subscription.component.scss',
})
export class CreateSubscriptionComponent implements OnInit {
  form: FormGroup;
  typeOptions: string[] = ['artist', 'genre'];
  artists: { id: string; name: string }[] = [];
  genres: string[] = [];
  dropdownOptions: string[] = [];

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<CreateSubscriptionComponent>
  ) {
    this.form = this.fb.group({
      type: ['artist', Validators.required],
      targetId: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.loadDropdownOptions();

    this.form.get('type')?.valueChanges.subscribe(() => {
      this.form.get('targetId')?.setValue('');
      this.loadDropdownOptions();
    });
  }

  loadDropdownOptions(): void {
    const type = this.form.get('type')?.value;

    // TODO: services
    if (type === 'artist') {
      this.artists = [
        { id: 'artist123', name: 'ArtistName' },
        { id: 'artist1234', name: 'ArtistName2' },
      ];
      this.dropdownOptions = this.artists.map((a) => a.name);
    } else {
      this.genres = ['pop', 'rock'];
      this.dropdownOptions = this.genres;
    }
  }

  async submit(): Promise<void> {
    if (!this.form.valid) return;

    const value = this.form.value;

    const subscriptionDto: CreateSubscription = {
      targetId: value.targetId,
      targetType: value.type,
    };

    this.dialogRef.close(subscriptionDto);
  }

  cancel(): void {
    this.dialogRef.close();
  }
}
