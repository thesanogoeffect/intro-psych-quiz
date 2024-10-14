<template>
  <v-container>
    <!-- Card for the question -->
    <v-card class="mb-4">
      <v-card-text>
        <p class="question-text" v-if="questionStore.currentlyReviewedQuestion">{{ questionStore.currentlyReviewedQuestion.question_title }}</p>
      </v-card-text>
    </v-card>

    <!-- Card wrapping the answer options -->
    <v-row justify="center">
      <v-col cols="12">
        <v-row
          v-for="(option, index) in answerOptions"
          :key="index"
          class="d-flex align-center answer-row"
        >
          <v-col cols="12">
            <v-card
              class="answer-card"
              :elevation="2"
              :class="{
                'correct-answer': isCorrectAnswer(index) && !questionStore.currentlyReviewedQuestion.skipped,
                'skipped-correct-answer': isCorrectAnswer(index) && questionStore.currentlyReviewedQuestion.skipped,
                'incorrect-guess': isIncorrectGuess(index),
                'correct-guess': isCorrectGuess(index),
              }"
            >
              <v-row class="d-flex align-center">
                <!-- Letter label (A, B, C, D) inside the card -->
                <v-col cols="auto">
                  <div class="answer-label ma-1">
                    {{ option.label }}
                  </div>
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
  </v-container>
</template>

<script>
import { defineComponent, computed } from "vue";
import { useQuestionStore } from "#imports";

export default defineComponent({
  name: "ReviewQuestionWindow",
  setup() {
    const questionStore = useQuestionStore();
    // questionStore.currentlyReviewedQuestion has the following extra parameters: .skipped (boolean), correct_answer_index (int), and guessed_index (int)

    const answerOptions = computed(() => {
      if (!questionStore.currentlyReviewedQuestion) {
        return [];
      }
      return questionStore.currentlyReviewedQuestion.answers.map((answer, index) => ({
        label: String.fromCharCode(65 + index), // Convert index to letter (A, B, C, D, ...)
        text: answer,
      }));
    });

    const isCorrectAnswer = (index) => {
      return index === questionStore.currentlyReviewedQuestion.correct_answer_index;
    };

    const isIncorrectGuess = (index) => {
      return index === questionStore.currentlyReviewedQuestion.guessed_index && index !== questionStore.currentlyReviewedQuestion.correct_answer_index;
    };

    const isCorrectGuess = (index) => {
      return index === questionStore.currentlyReviewedQuestion.guessed_index && index === questionStore.currentlyReviewedQuestion.correct_answer_index;
    };

    return {
      questionStore,
      answerOptions,
      isCorrectAnswer,
      isIncorrectGuess,
      isCorrectGuess,
    };
  },
});
</script>

<style scoped>
.question-text {
  font-size: 1.35rem;
  font-weight: 500;
  margin-bottom: 1rem;
  text-align: center;
}

.answer-row {
  margin-bottom: 1rem;
}

.answer-card {
  padding: 1.15rem; /* Added extra padding to increase the size */
  transition: all 0.3s ease;
  cursor: default;
}

.answer-label {
  font-size: 1.3rem; /* Slightly increased label font size */
  font-weight: 500;
  color: #C81919;
}

.answer-text {
  font-size: 1.2rem; /* Slightly increased text size */
}

/* Correct answer (highlighted green if not skipped) */
.correct-answer {
  background-color: #4caf50; /* Vuetify success color */
  color: white;
}

/* Skipped correct answer (light green) */
.skipped-correct-answer {
  background-color: #c8e6c9; /* Light green */
  color: black;
}

/* Incorrect guess (highlighted red) */
.incorrect-guess {
  background-color: #ff9800; /* Vuetify warn color */
  color: white;
}

/* Correct guess (highlighted green) */
.correct-guess {
  background-color: #4caf50; /* Vuetify success color */
  color: white;
}
</style>
