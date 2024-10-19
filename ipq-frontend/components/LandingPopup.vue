<template>
  <v-dialog
    v-model="generalStore.landingPopup"
    max-width="800px"
    persistent
    v-if="!mobile.value"
  >
    <v-card class="rounded-xl">
      <v-card-title class="headline text-center">Welcome!</v-card-title>
      <v-card-text class="mx-4">
        <p>
          Hi, welcome to the Intro to Psychology Quiz. I hope you find it
          useful!
        </p>
        <p>
          Please upvote, downvote and flag as much as possible. It means we all
          have better questions 🙏
        </p>
        <p>You can find instructions and more info in the top menu.</p>
        <h3><strong>Disclaimer:</strong></h3>
        <p>
          Some of the questions <b>might be incorrect</b>, please flag them if
          you think so. For wrong chapters, please rather use the report button in the chapter info. 
        </p>
        <h3><strong>News:</strong></h3>
        <ul>
            <li>The app is officially out since 21-10-2024! 🎉</li>
          <li>
            New feature - You can now see a <b>ChatGPT explanation</b> after answering a
            question. Try it out in the right sidebar!
          </li>
          <li>
            Halfway student-made questions from 21-22 have been added in, there
            are more to come 😊
          </li>
        </ul>
        <v-container class="text-center">
          <v-btn color="primary" @click="closeDialog">Sounds good</v-btn>
          <br />
        </v-container>
        <br />

        <p>
          If you have any feedback or want to support the project, check the
          /about page ❤️
        </p>
        <br />

        <p>
          Enjoy! <br />
          Jakub
        </p>
      </v-card-text>
    </v-card>
  </v-dialog>
  <v-dialog
    v-model="generalStore.landingPopup"
    max-width="800px"
    v-else
    persistent="true"
  >
    <v-card class="rounded-xl">
      <v-card-title class="headline text-center">Welcome!</v-card-title>
      <v-card-text class="mx-4">
        <p>Hi, welcome to the Intro to Psychology Quiz.</p>
        <p>
          Unfortunately, the app doesn't yet work on mobile, sorry. 😞 Please
          visit from a larger screen device.
        </p>

        <p>
          See you there! <br />
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
    const mobile = computed(() => display.mobile);

    const closeDialog = () => {
      generalStore.toggleLandingPopup();
    };

    onMounted(() => {
      generalStore.checkLandingPopup();
    });

    return {
      closeDialog,
      generalStore,
      mdAndUp,
      mobile,
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
