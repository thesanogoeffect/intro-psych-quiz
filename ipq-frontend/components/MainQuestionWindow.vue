<template>
  <v-container :style="containerStyle">
    <v-container :style="innerContainerStyle">
      <!-- Container now has margin auto for centering -->
      <v-row justify="center">
        <GuessQuestionWindow v-if="!questionStore.reviewMode"></GuessQuestionWindow>
        <ReviewQuestionWindow v-else></ReviewQuestionWindow>
        <QuestionNavigation></QuestionNavigation>
      </v-row>
    </v-container>
  </v-container>
</template>

<script>
import { defineComponent, computed } from "vue";
import { useQuestionStore } from "#imports";
import GuessQuestionWindow from "./GuessQuestionWindow.vue";
import ReviewQuestionWindow from "./ReviewQuestionWindow.vue";
import QuestionNavigation from "./QuestionNavigation.vue";
import { useDisplay } from "#imports";

export default defineComponent({
  name: "MainQuestionWindow",
  components: {
    GuessQuestionWindow,
    ReviewQuestionWindow,
    QuestionNavigation,
  },
  setup() {
    const questionStore = useQuestionStore();
    const display = useDisplay();

    const containerStyle = computed(() => ({
      maxWidth: "1000px",
      margin: "auto",
      maxHeight: "610px",
    }));

    const innerContainerStyle = computed(() => ({
      transform: display.mdAndUp.value ? "scale(0.9)" : "scale(0.7)",
      transformOrigin: "top left",
    }));

    return {
      questionStore,
      containerStyle,
      innerContainerStyle,
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