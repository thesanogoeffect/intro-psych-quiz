<template>
  <v-container style="max-width: 1000px; margin: auto; max-height: 610px">
    <v-container style="transform: scale(0.9); transform-origin: top left">
      <!-- Container now has margin auto for centering -->
      <v-row justify="center">
        <GuessQuestionWindow v-if="!questionStore.reviewMode"></GuessQuestionWindow>
        <ReviewQuestionWindow v-else></ReviewQuestionWindow>
        <QuestionNavigation ></QuestionNavigation>
      </v-row>
    </v-container>
  </v-container>
</template>

<script>
import { defineComponent } from "vue";
import { useQuestionStore } from "#imports";
import GuessQuestionWindow from "./GuessQuestionWindow.vue";
import ReviewQuestionWindow from "./ReviewQuestionWindow.vue";
import QuestionNavigation from "./QuestionNavigation.vue";

export default defineComponent({
  name: "MainQuestionWindow",
  components: {
    GuessQuestionWindow,
    ReviewQuestionWindow,
    QuestionNavigation,
  },
  setup() {
    const questionStore = useQuestionStore();
    return {
      questionStore,
      GuessQuestionWindow,
      ReviewQuestionWindow,
      QuestionNavigation,
    };
  },
});
</script>

<style scoped>
/* Optional: Ensure v-row does not have extra padding or margins */
v-row {
  margin: 0;
  padding: 0;
}
</style>
