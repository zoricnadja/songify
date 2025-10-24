import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CreateSubscription } from '../subscription.model';
import { GenreService } from '../../genre/genre.service';
import { ArtistService } from '../../artist/artist.service';
import { Artist } from '../../artist/models/artist.model';

@Component({
  selector: 'app-create-subscription',
  standalone: false,
  templateUrl: './create-subscription.component.html',
  styleUrl: './create-subscription.component.scss',
})
export class CreateSubscriptionComponent implements OnInit {
  form: FormGroup;
  typeOptions: string[] = ['artist', 'genre'];
  artists: Artist[] = [];
  genres: string[] = [];
  selectedArtistIds: string[] = [];
  selectedGenres: string[] = [];
  dropdownOptions: string[] = [];

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<CreateSubscriptionComponent>,
    private genreService: GenreService,
    private artistService: ArtistService
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
    if (type === 'artist') {
      this.artistService.getArtists().subscribe((artists) => {
        this.artists = artists;
      });
      this.dropdownOptions = this.artists.map((a) => a.name);
    } else {
      this.genreService.getAll().subscribe((genres) => {
        this.genres = genres;
      });
      this.dropdownOptions = this.genres;
    }
  }

  async submit(): Promise<void> {
    if (!this.form.valid) return;

    const value = this.form.value;
    const name =
      value.type == 'artist'
        ? this.artists.find((a) => (a.id = value.targetId))?.name
        : value.targetId;

    const subscriptionDto: CreateSubscription = {
      targetId: value.targetId,
      targetType: value.type,
      targetName: name,
    };

    this.dialogRef.close(subscriptionDto);
  }

  cancel(): void {
    this.dialogRef.close();
  }
}
