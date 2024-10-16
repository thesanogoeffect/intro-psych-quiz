<template>
  <v-container v-if="currentQuestion" class="py-3">
    <v-row>
      <v-col>
        <div class="stats-container pa-3">
          <h2 class="mb-2 text-center">Question Info</h2>

          <!-- Question ID on top -->
          <v-row>
            <v-col>
              <v-icon color="info">mdi-pound</v-icon>
              ID: {{ currentQuestionId }}
            </v-col>
          </v-row>

          <!-- Chapter Number and Name second -->
          <v-row>
            <v-col>
              <v-icon color="primary">mdi-book</v-icon>
              Chapter: {{ chapter ? chapterId + ' - ' + chapter : 'Unknown Chapter' }}
            </v-col>
          </v-row>

          <!-- Source -->
          <v-row>
            <v-col>
              <v-icon color="secondary">mdi-book-open-page-variant</v-icon>
              Source: {{ source || 'N/A' }}
            </v-col>
          </v-row>

          <!-- Author -->
          <v-row>
            <v-col>
              <v-icon color="primary">mdi-account</v-icon>
              Author: {{ author || '-' }}
            </v-col>
          </v-row>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { computed } from 'vue';
import { useQuestionStore } from '#imports';

export default {
  name: 'RightSidebar',
  setup() {
    const questionStore = useQuestionStore();

    const currentQuestion = computed(() =>
      questionStore.getReviewMode
        ? questionStore.getCurrentlyReviewedQuestion
        : questionStore.getCurrentQuestion
    );
    const currentQuestionId = computed(() => currentQuestion.value.id);

    const author = computed(() => currentQuestion.value.author);
    const source = computed(() => currentQuestion.value.source);
    const chapterId = computed(() => currentQuestion.value.chapter_id);
    const chapter = computed(() =>
      questionStore.getChapterById(chapterId.value)
    );

    return {
      currentQuestion,
      currentQuestionId,
      author,
      source,
      chapterId,
      chapter,
    };
  },
};
</script>

<style scoped>
.stats-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  font-weight: bold;
  font-size: 1.5rem;
}

.v-row {
  margin-bottom: 10px;
}

.v-icon {
  margin-right: 5px;
}
</style>
