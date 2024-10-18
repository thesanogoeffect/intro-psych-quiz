<template>
  <v-dialog v-model="generalStore.landingPopup" max-width="800px">
    <v-card class="rounded-xl">
      <v-card-title class="headline text-center">Welcome!</v-card-title>
      <v-card-text class="mx-4">
        <p>
          Hi, welcome to the preview version of the Intro to Psychology Quiz. I
          hope you find it useful!
        </p>
        <p>
          You can find instructions and more info in the top menu.
        </p>
        <h3><strong>Disclaimer:</strong></h3>
        <p>
          Some of the questions <b>might be incorrect</b>, please flag them if you
          think so.
        </p>
        <p>
          As the app is in a preview state, there might be some issues. If you
          find any, please let me know.
        </p>
        <h3><strong>News:</strong></h3>
        <ul>
          <li>
            We are getting closer to a full release on 21-10-2024!
           
          </li>
          <li> The mobile version is still not functional, I'm working on it 💪</li>
        </ul>
        <v-container v-if="!mdAndUp.value" class="text-center">
        <v-btn color="primary" @click="closeDialog">Sounds good</v-btn>
        <br />
        </v-container>
        <br />

        <p>If you have any feedback or want to support the project, check the /about page ❤️</p>
        <br />


        <p>
          Enjoy! <br />
          Jakub
        </p>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, onMounted } from "vue";
import { useGeneralStore } from "~/stores/generalstore";
import { useDisplay } from "#imports";
export default {
  name: "LandingPopup",
  setup() {
    const generalStore = useGeneralStore();
    const display = useDisplay();
    const mdAndUp = computed(() => display.mdAndUp);

    const closeDialog = () => {
      generalStore.toggleLandingPopup();
    };

    return {
      closeDialog,
      generalStore,
      mdAndUp,
    };
  },
};
</script>

<style scoped>
.notice {
  font-size: 0.8rem;
  color: gray;
}
</style>
