<template>
  <v-container style="max-width: 1000px; margin: auto; max-height: 610px;">
    <v-container style="transform: scale(0.9); transform-origin: top left;"> <!-- Added scale option here -->
      <v-row justify="center">
        <GuessQuestionWindow></GuessQuestionWindow>
      </v-row>
    <QuestionNavigation></QuestionNavigation>

    </v-container>
  </v-container>
</template>

<script>
import { defineComponent } from 'vue';
import { useQuestionStore } from '#imports';
import GuessQuestionWindow from './GuessQuestionWindow.vue';
import ReviewQuestionWindow from './ReviewQuestionWindow.vue';
import QuestionNavigation from './QuestionNavigation.vue';

export default defineComponent({
  name: 'MainQuestionWindow',
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
/* Add any custom styling if needed */
</style>
