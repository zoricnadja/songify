import { Component, OnInit } from '@angular/core';
import { TrackService } from '../track.service';

@Component({
  selector: 'app-track-player-list',
  standalone: false,
  templateUrl: './track-player-list.component.html',
  styleUrls: ['./track-player-list.component.scss']
})
export class TrackPlayerListComponent implements OnInit {
  tracks: any[] = [];

  constructor(private trackService: TrackService) {}

  ngOnInit() {
    this.trackService.getTracks().subscribe(tracks => {
      this.tracks = tracks;
    });
  }
}

