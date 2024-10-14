// vuetify.config.ts
import { defineVuetifyConfiguration } from "vuetify-nuxt-module/custom-configuration";

export default defineVuetifyConfiguration({
  theme: {
    defaultTheme: "light",
    themes: {
      light: {
        colors: {
          primary: "#C81919",
          background: "#C81919",
        },
      },
      dark: {
        colors: {
          primary: "#C81919",
          background: "#C81919",
        },
      },
    },
  },
});
