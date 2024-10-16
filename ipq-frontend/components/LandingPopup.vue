<template>
  <v-dialog v-model="generalStore.landingPopup" max-width="800px">
    <v-card>
      <v-card-title class="headline text-center">Welcome!</v-card-title>
      <v-card-text class="mx-4">
        <p>
          Hi, welcome to the preview version of the Intro to Psychology Quiz. I
          hope you find it useful!
        </p>
        <p>
          You can find instructions and more info in the top menu.
        </p>
        <p><strong>Disclaimer:</strong></p>
        <p>
          Some of the questions <b>might be incorrect</b>, please flag them if you
          think so.
        </p>
        <p>
          As the app is in a preview state, there might be some issues. If you
          find any, please let me know.
        </p>
        <p><strong>Current Status:</strong></p>
        <ul>
          <li>
            We are getting closer to a full release on 21-10-2024!
            The app currently still doesn't work on mobile, but I'm working on it.
          </li>
        </ul>
        <v-btn color="primary" @click="closeDialog">Sounds good</v-btn>
        <br />
        <p>
          Good luck, <br />
          Jakub
        </p>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, onMounted } from "vue";
import { useGeneralStore } from "~/stores/generalstore";
export default {
  name: "LandingPopup",
  setup() {
    const generalStore = useGeneralStore();

    const closeDialog = () => {
      generalStore.toggleLandingPopup();
    };

    return {
      closeDialog,
      generalStore,
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
