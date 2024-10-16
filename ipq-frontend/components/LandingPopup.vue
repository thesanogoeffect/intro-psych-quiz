<template>
  <v-dialog v-model="welcomeDialog" max-width="800px" persisent>
    <v-card>
      <v-card-title class="headline">Welcome!</v-card-title>
      <v-card-text>
        <p>
          Hi, welcome to the preview version of the Intro to Psychology Quiz. I
          hope you find it useful!
        </p>
        <p><strong>Instructions:</strong></p>
        <ol>
          <li>
            Use the left-right arrows (or A and D keys) to navigate through
            questions.
          </li>
          <li>
            The right arrow works as a "Skip" button if you don't know the
            answer. You only get 3 skips, but you might earn more by doing well.
          </li>
          <li>
            Flag questions that seem incorrect so they can be reviewed by an LLM
            or me.
          </li>
          <li>
            You can upvote/downvote questions to improve question quality for
            everyone.
          </li>
        </ol>

        <p><strong>Top menu:</strong></p>
        <ul>
          <li>You can filter questions by chapters or by source.</li>
          <li>
            There is an About page, where you can find more info and how to
            contact me if needed.
          </li>
          <li>
            The dark mode is under construction, but you can try it in the top
            menu!
          </li>
          <li>
            You can toggle the stats/info sidebars by clicking the icons on the
            sides.
          </li>
        </ul>

        <p><strong>Disclaimer:</strong></p>
        <p>
          Some of the questions might be incorrect, please flag them if you
          think so. This is currently not an official part of the TU/e course,
          just a passion project. I am not responsible for any mistakes or
          inaccuracies.
        </p>
        <p>
          As the app is in a preview state, there might be some issues. If you
          find any, please let me know.
        </p>

        <p><strong>Other notes:</strong></p>
        <ul>
          <li>
            The app currently doesn't work on mobile and doesn't have a
            colorblind mode (please get in touch if you need it).
          </li>
        </ul>

        <p class="notice">
          I use 🍪 to remember if you have seen this, and won't show it to you
          again. You can always find it in the top menu.
        </p>
        <v-btn color="primary" @click="closeDialog">I agree</v-btn>
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
    const welcomeDialog = computed(() => generalStore.getLandingPopup);

    const closeDialog = () => {
      generalStore.toggleLandingPopup();
      localStorage.setItem("hasSeenWelcomeDialog", "true");
    };
    onMounted(() => {
      const hasSeenWelcomeDialog = localStorage.getItem("hasSeenWelcomeDialog");
      if (!hasSeenWelcomeDialog) {
        welcomeDialog.value = true;
      }
    });
    return {
      welcomeDialog,
      closeDialog,
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
