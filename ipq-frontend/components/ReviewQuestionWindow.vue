<template>
  <v-container :style="containerStyle">
    <!-- Card for the question -->
    <v-card class="rounded-xl" elevation="1">
      <!-- Question area -->
      <v-card class="mb-4 text-h3 rounded-lg" elevation="0">
        <v-card-text>
          <p class="question-text" v-if="questionStore.currentlyReviewedQuestion">
            {{ questionStore.currentlyReviewedQuestion.question_title }}
          </p>
        </v-card-text>
      </v-card>

      <v-divider></v-divider>

      <!-- Answer options -->
      <v-card class="ma-4 pa-6" elevation="0">
        <v-row>
          <v-col cols="12" class="align-center">
            <v-row
              v-for="(option, index) in answerOptions"
              :key="index"
              class="align-center answer-row"
            >
              <v-col cols="12">
                <v-card
                  class="answer-card rounded-pill"
                  :elevation="2"
                  :class="{
                    'correct-answer':
                      isCorrectAnswer(index) &&
                      !questionStore.currentlyReviewedQuestion.skipped,
                    'skipped-correct-answer':
                      isCorrectAnswer(index) &&
                      questionStore.currentlyReviewedQuestion.skipped,
                    'incorrect-guess': isIncorrectGuess(index),
                    'correct-guess': isCorrectGuess(index),
                  }"
                >
                  <v-row class="d-flex align-center">
                    <!-- Button-like label (A, B, C, D) inside the card -->
                    <v-col cols="auto">
                      <v-btn
                        class="ma-1 answer-button"
                        text
                        color="primary"
                      >
                        {{ option.label }}
                      </v-btn>
                    </v-col>
                    <!-- Text of the answer inside the card -->
                    <v-col>
                      <p class="answer-text">{{ option.text }}</p>
                    </v-col>
                  </v-row>
                </v-card>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-card>
  </v-container>
</template>

<script>
import { defineComponent, computed } from "vue";
import { useQuestionStore, useDisplay } from "#imports";

export default defineComponent({
  name: "ReviewQuestionWindow",
  setup() {
    const questionStore = useQuestionStore();
    const display = useDisplay();

    const answerOptions = computed(() => {
      if (!questionStore.currentlyReviewedQuestion) {
        return [];
      }
      return questionStore.currentlyReviewedQuestion.answers.map(
        (answer, index) => ({
          label: String.fromCharCode(65 + index), // A, B, C, D...
          text: answer,
        })
      );
    });

    const isCorrectAnswer = (index) => {
      return (
        index === questionStore.currentlyReviewedQuestion.correct_answer_index
      );
    };

    const isIncorrectGuess = (index) => {
      return (
        index === questionStore.currentlyReviewedQuestion.guessed_index &&
        index !== questionStore.currentlyReviewedQuestion.correct_answer_index
      );
    };

    const isCorrectGuess = (index) => {
      return (
        index === questionStore.currentlyReviewedQuestion.guessed_index &&
        index === questionStore.currentlyReviewedQuestion.correct_answer_index
      );
    };

    const containerStyle = computed(() => ({
      transform: display.mdAndUp.value ? "scale(1)" : "scale(0.8)",
      transformOrigin: "top left",
    }));

    return {
      questionStore,
      answerOptions,
      isCorrectAnswer,
      isIncorrectGuess,
      isCorrectGuess,
      containerStyle,
    };
  },
});
</script>

<style scoped>
.question-text {
  font-size: 1.4rem;
  font-weight: 500;
  margin-bottom: 1rem;
  text-align: center;
}

.answer-card {
  cursor: default;
  padding: 1rem;
  transition: all 0.3s ease;
}

.answer-button {
  font-size: 1.2rem;
}

.answer-text {
  font-size: 1.2rem;
}

/* Styling for different answer states */
.correct-answer {
  background-color: #4caf50; /* Vuetify success color */
  color: white;
}

.skipped-correct-answer {
  background-color: #c8e6c9; /* Light green */
  color: black;
}

.incorrect-guess {
  background-color: #ff9800; /* Vuetify warning color */
  color: white;
}

.correct-guess {
  background-color: #4caf50; /* Vuetify success color */
  color: white;
}
</style>
