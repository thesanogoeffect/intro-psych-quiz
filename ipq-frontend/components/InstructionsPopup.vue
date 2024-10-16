<template>
  <v-dialog v-model="generalStore.instructionsPopup" max-width="800px">
    <v-card>
      <v-card-title class="headline text-center">Help</v-card-title>
      <v-card-text class="mx-4">
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

        <v-btn color="primary" @click="closeDialog">Sounds good</v-btn>
        <br />
        <p class="">
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
  name: "InstructionsPopup",
  setup() {
    const generalStore = useGeneralStore();

    const closeDialog = () => {
      generalStore.toggleInstructionsPopup();
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
  