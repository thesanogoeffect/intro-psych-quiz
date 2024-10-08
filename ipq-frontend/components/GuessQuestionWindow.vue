<template>
  <v-container>
    <!-- Card for the question -->
    <v-card class="mb-4">
      <v-card-text>
        <p class="question-text">{{ questionStore.getCurrentQuestion.question_title }}</p>
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
            <v-card class="answer-card" @click="handleAnswer(index)" elevation="2">
              <v-row class="d-flex align-center">
                <!-- Button-like label (A, B, C, D) inside the card -->
                <v-col cols="auto">
                  <v-btn class="ma-1" text color="primary" style="font-size: 1.2rem">
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
  </v-container>
</template>

<script>
import { defineComponent, computed } from 'vue';
import { useQuestionStore } from '#imports';

export default defineComponent({
  name: 'GuessQuestionWindow',
  setup() {
    const questionStore = useQuestionStore();

    const answerOptions = computed(() => {
      const currentQuestion = questionStore.getCurrentQuestion;
      if (!currentQuestion) {
        return [];
      }
      return currentQuestion.answers.map((answer, index) => ({
        label: String.fromCharCode(65 + index), // Convert index to letter (A, B, C, D, ...)
        text: answer,
      }));
    });

    const handleAnswer = async (index) => {
      console.log('Selected answer index:', index);
      await questionStore.answerCurrentQuestion(index);
    };

    return {
      questionStore,
      answerOptions,
      handleAnswer,
    };
  },
});
</script>

<style scoped>
.question-text {
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: 1rem;
  text-align: center;
}

.answer-row {
  margin-bottom: 1rem;
}

.answer-card {
  cursor: pointer;
  padding: 1rem;
  transition: all 0.3s ease;
}

.answer-card:hover {
  background-color: #f1f1f1;
}

.answer-text {
  font-size: 1.1rem;
}
</style>
