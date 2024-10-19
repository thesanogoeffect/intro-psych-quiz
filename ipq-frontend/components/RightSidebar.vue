<template>
  <v-container v-if="currentQuestion" class="py-3">
    <v-row>
      <v-col>
        <v-container class="stats-container pa-3 rounded-xl">
          <h2 class="mb-2 text-center">Question Details</h2>

          <!-- Question ID on top -->
          <v-row>
            <v-col>
              <v-icon color="info">mdi-pound</v-icon>
              ID: {{ currentQuestionId }}
            </v-col>
          </v-row>

          <!-- Chapter Number and Name second, with report icon -->
          <v-row>
            <v-col cols="9">
              <v-icon color="primary">mdi-book</v-icon>
              Chapter:
              {{ chapter ? chapterId + " - " + chapter : "Unknown Chapter" }}
            </v-col>
            <v-col class="d-flex justify-end align-center">
              <a :href="reportLink" target="_blank" title="Report wrong chapter">
                <v-icon color="red">mdi-alert-circle</v-icon>
              </a>
            </v-col>
          </v-row>

          <!-- Source -->
          <v-row>
            <v-col>
              <v-icon color="secondary">mdi-book-open-page-variant</v-icon>
              Source: {{ source || "N/A" }}
            </v-col>
          </v-row>

          <!-- Author -->
          <v-row>
            <v-col>
              <v-icon color="primary">mdi-account</v-icon>
              Author: {{ author || "-" }}
            </v-col>
          </v-row>
        </v-container>
      </v-col>
      <v-expansion-panels v-if="questionStore.getReviewMode">
        <v-expansion-panel class="rounded-lg" title="ChatGPT Explanation">
          <v-expansion-panel-text>
            <span v-html="llmExplanation"></span>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-row>
  </v-container>
</template>



<script>
import { computed } from "vue";
import { useQuestionStore } from "#imports";

export default {
  name: "RightSidebar",
  setup() {
    const questionStore = useQuestionStore();

    const currentQuestion = computed(() =>
      questionStore.getReviewMode
        ? questionStore.getCurrentlyReviewedQuestion
        : questionStore.getCurrentQuestion
    );
    const currentQuestionId = computed(() => currentQuestion.value.id);
    const chapterId = computed(() => currentQuestion.value.chapter_id);
    const chapter = computed(() =>
      questionStore.getChapterById(chapterId.value)
    );
    
    const reportLink = computed(() => {
      const baseURL = "https://docs.google.com/forms/d/e/1FAIpQLSf5j48KtwqNV3KWKYvMh6xSR3xeYgkv0TyguVvJ0jLav3s3-g/viewform?usp=pp_url";
      const params = new URLSearchParams();
      params.append("entry.366340186", currentQuestionId.value);
      params.append("entry.568292540", chapterId.value);
      return `${baseURL}&${params.toString()}`;
    });

    return {
      currentQuestion,
      currentQuestionId,
      chapterId,
      chapter,
      reportLink,
      questionStore,
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
