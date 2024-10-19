<template>
  <v-container :style="containerStyle">
    <!-- Card for the question -->
    <v-card class="rounded-xl middle-card" elevation="1">
      <!-- Question area -->
      <v-card class="mb-4 text-h3 rounded-lg" elevation="0">
        <v-card-text>
          <p class="question-text">
            {{ questionStore.getCurrentQuestion.question_title }}
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
                  @click="handleAnswer(index)"
                  elevation="2"
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
import { useQuestionStore } from "#imports";
import { useDisplay } from "#imports";
import "@/assets/global.css";

export default defineComponent({
  name: "GuessQuestionWindow",
  setup() {
    const questionStore = useQuestionStore();
    const display = useDisplay();

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
      console.log("Selected answer index:", index);
      await questionStore.answerCurrentQuestion(index);
    };

    const containerStyle = computed(() => ({
      transform: display.mdAndUp.value ? "scale(1)" : "scale(0.8)",
      transformOrigin: "top left",
    }));

    return {
      questionStore,
      answerOptions,
      handleAnswer,
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
  cursor: pointer;
  padding: 1rem;
  transition: all 0.3s ease;
}

.answer-button {
  font-size: 1.2rem;
}

.answer-text {
  font-size: 1.2rem;
}
</style>
