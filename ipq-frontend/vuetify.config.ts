// vuetify.config.ts
import { defineVuetifyConfiguration } from 'vuetify-nuxt-module/custom-configuration'

export default defineVuetifyConfiguration({
    // use TU/e Scarlet from the manual: HEX C81919
    theme: {
        defaultTheme: 'light',
        themes: {
          light: { 
            colors: {
              primary: '#C81919'
            } 
          },
          dark: { 
            colors: {
              primary: '#C81919'
            } 
          },
        },
      },
})