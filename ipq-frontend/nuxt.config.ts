import { Title } from "#build/components";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  devtools: { enabled: true },
  ssr: false,
  modules: ["@pinia/nuxt", "vuetify-nuxt-module"],
  hooks: {
    "prerender:routes"({ routes }) {
      routes.clear(); // Do not generate any routes (except the defaults)
    },
  },
  // app: {
  //   baseURL: "/intro-psych-quiz/", // Change this to your repository's name
  // },

  // runtimeConfig: {
  //   public: {
  //     baseURL: "https://thesanogoeffect.github.io/intro-psych-quiz/",
  //   },
  // },

  vuetify: {
    vuetifyOptions: "./vuetify.config.ts",
  },
});
