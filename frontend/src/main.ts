import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { Amplify } from 'aws-amplify';
import { AppModule } from './app/app.module';

platformBrowserDynamic()
  .bootstrapModule(AppModule, {
    ngZoneEventCoalescing: true,
  })
  .catch((err: Error) => console.error(err));

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: 'eu-central-1_dMyCdtFX9',
      userPoolClientId: 'e03ermp6cpmqdrg9g4vhjtlgs',
    },
  },
});
