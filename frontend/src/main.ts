import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import awsAmplify from 'aws-amplify';
import { AppModule } from './app/app.module';

platformBrowserDynamic()
  .bootstrapModule(AppModule, {
    ngZoneEventCoalescing: true,
  })
  .catch((err) => console.error(err));

awsAmplify.Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: 'eu-central-1_dMyCdtFX9',
      userPoolClientId: '3q79gv4rgi7cd4qu3a7npnl72c',
    },
  },
});
