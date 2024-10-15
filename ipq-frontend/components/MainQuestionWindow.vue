<template>
  <v-container fluid class="main-container">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <GuessQuestionWindow v-if="!questionStore.reviewMode" />
        <ReviewQuestionWindow v-else />
        <QuestionNavigation />
      </v-col>
    </v-row>
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
    };
  },
});
</script>

<style scoped>
.main-container {
  margin: auto;
  padding: 16px; /* Optional: Adjust padding as needed */
}

/* Remove unnecessary styles */
</style>
