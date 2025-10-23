import { Component, OnInit } from '@angular/core';
import { TrackService } from '../track.service';
import { MatDialog } from '@angular/material/dialog';
import { TrackModalComponent } from '../track-modal/track-modal.component';
import { Track } from '../models/track.model';

@Component({
  selector: 'app-track-list',
  standalone: false,
  templateUrl: './track-list.component.html',
  styleUrl: './track-list.component.scss'
})
export class TrackListComponent implements OnInit {
  tracks: Track[] = [];

  constructor(private trackService: TrackService, private dialog: MatDialog) {}

  ngOnInit() {
    this.loadTracks();
  }

  loadTracks() {
    this.trackService.getTracks().subscribe(tracks => {
      this.tracks = tracks;
    });
  }

  openCreateModal() {
    this.dialog.open(TrackModalComponent, {
      width: '600px',
      data: { title: '', genres: [], artists: [], album: '', image: '', track: '', fileInfo: {} }
    }).afterClosed().subscribe(result => {
      if (result) {
        this.trackService.createTrack(result).subscribe(() => this.loadTracks());
      }
    });
  }

  openEditModal(track: any) {
    this.dialog.open(TrackModalComponent, {
      width: '600px',
      data: { ...track }
    }).afterClosed().subscribe(result => {
      if (result) {
        this.trackService.updateTrack(track.id, result).subscribe(() => this.loadTracks());
      }
    });
  }

  deleteTrack(track: any) {
    if (confirm('Are you sure you want to delete this track?')) {
      this.trackService.deleteTrack(track.id).subscribe(() => this.loadTracks());
    }
  }
}
