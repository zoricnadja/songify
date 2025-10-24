import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LayoutModule } from './layout/layout.module';
import { AuthModule } from './auth/auth.module';
import { HTTP_INTERCEPTORS, provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { AuthInterceptor } from './auth/interceptor';
import { AuthGuard } from './auth/auth.guard';
import { AlbumModule } from './album/album.module';
import { ArtistModule } from './artist/artist.module';
import { GenreModule } from './genre/genre.module';
import { TrackModule } from './track/track.module';
import { AdminModule } from './admin/admin.module';
import { MaterialModule } from './infrastructure/material/material.module';
import { SubscriptionModule } from './subscription/subscription.module';
import { DiscoverModule } from './discover/discover.module';

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AdminModule,
    AlbumModule,
    ArtistModule,
    AuthModule,
    GenreModule,
    LayoutModule,
    MaterialModule,
    TrackModule,
    SubscriptionModule,
    DiscoverModule,
  ],
  providers: [
    AuthGuard,
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    provideHttpClient(withInterceptorsFromDi()),
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
