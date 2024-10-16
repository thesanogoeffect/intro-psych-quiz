<template>
  <v-container v-if="isStoreInitialized" class="py-3">
    <v-row>
      <v-col>
        <div class="stats-container pa-3">
          <h2 class="mb-2 text-center">Stats</h2>
          <!-- Existing User Stats -->
          <v-row>
            <v-col cols="2" xs="3">
              <v-icon color="secondary">mdi-eye-outline</v-icon>
            </v-col>
            <v-col cols="7" xs="6"> Total Shown: </v-col>
            <v-col cols="3" xs="3">
              {{ userStore.getTotalShownQuestions }}
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="2" xs="3">
              <v-icon color="primary">mdi-checkbox-marked-circle-outline</v-icon>
            </v-col>
            <v-col cols="7" xs="6"> Answered: </v-col>
            <v-col cols="3" xs="3">
              {{ userStore.getTotalAnsweredQuestions }}
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="2" xs="3">
              <v-icon color="success">mdi-check-circle-outline</v-icon>
            </v-col>
            <v-col cols="7" xs="6"> Correct: </v-col>
            <v-col cols="3" xs="3">
              {{ userStore.getTotalCorrectAnswers }}
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="2" xs="3">
              <v-icon color="warning">mdi-skip-next-circle-outline</v-icon>
            </v-col>
            <v-col cols="7" xs="6"> Skipped: </v-col>
            <v-col cols="3" xs="3">
              {{ userStore.getSkippedQuestions }}
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="2" xs="3">
              <v-icon color="info">mdi-help-circle-outline</v-icon>
            </v-col>
            <v-col cols="7" xs="6">Skips Left:</v-col>
            <v-col cols="3" xs="3"> {{ userStore.getSkipsRemaining }}</v-col>
          </v-row>
          <v-row
            v-show="userStore.getTotalAnsweredQuestions > 0"
            justify="center"
          >
            <v-col cols="12" class="text-center">
              <v-progress-circular
                :model-value="userPercentage"
                :color="circularColor"
                size="78"
                width="10"
              >
                <span :class="percentageClass">{{ formattedPercentage }}%</span>
              </v-progress-circular>
              <div>Your Correct Percentage</div>
            </v-col>
          </v-row>

          <!-- Toggle for Global Stats -->
          <v-row class="mt-4">
            <v-col cols="12">
              <v-switch
                v-model="showGlobalStats"
                label="Show Community Question Stats"
              ></v-switch>
            </v-col>
          </v-row>

          <!-- Global Stats Section -->
          <div v-if="showGlobalStats">
            <h2 class="mb-2 mt-4">Community Stats</h2>
            <h3 class="mb-3">
              {{ chapter ? chapter.name : "Unknown Chapter" }}
            </h3>
            <v-row>
              <v-col>
                <v-icon color="secondary">mdi-eye-outline</v-icon>
                Times Asked: {{ questionStats.times_asked }}
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-icon color="success">mdi-check-circle-outline</v-icon>
                Answered Correctly: {{ questionStats.times_answered_correct }}
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-icon color="primary">mdi-checkbox-marked-circle-outline</v-icon>
                Times Answered: {{ questionStats.times_answered }}
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-icon color="warning">mdi-skip-next-circle-outline</v-icon>
                Times Skipped: {{ questionStats.times_skipped }}
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-icon color="error">mdi-flag-outline</v-icon>
                Times Flagged: {{ questionStats.times_flagged }}
              </v-col>
            </v-row>
            <v-row v-show="questionStats.times_answered > 0" justify="center">
              <v-col cols="12" class="text-center">
                <v-progress-circular
                  :model-value="correctPercentage"
                  :color="globalCircularColor"
                  size="78"
                  width="10"
                >
                  <span :class="globalPercentageClass"
                    >{{ correctPercentage.toFixed(1) }}%</span
                  >
                </v-progress-circular>
                <div>Community Percentage</div>
              </v-col>
            </v-row>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useQuestionStore } from "#imports";
import { useQuestionStatsStore } from "#imports";

export default {
  data() {
    return {
      isStoreInitialized: false,
      userStore: null,
      questionStatsStore: null,
      showGlobalStats: false,
    };
  },
  created() {
    try {
      this.userStore = useQuestionStore();
      this.questionStatsStore = useQuestionStatsStore();
      this.isStoreInitialized = true;
    } catch (error) {
      console.error("Pinia store is not initialized:", error);
    }
  },
  computed: {
    // User Stats Computed Properties
    userPercentage() {
      return this.userStore.getAnsweredCorrectlyPercentage;
    },
    formattedPercentage() {
      return this.userPercentage.toFixed(1);
    },
    circularColor() {
      const percentage = this.userPercentage;
      if (percentage >= 70) {
        return "success"; // High percentage - green
      } else if (percentage >= 40) {
        return "warning"; // Medium percentage - yellow
      } else {
        return "error"; // Low percentage - red
      }
    },
    percentageClass() {
      const percentage = this.userPercentage;
      if (percentage >= 70) {
        return "text-success"; // Green text for high percentage
      } else if (percentage >= 40) {
        return "text-warning"; // Yellow text for medium percentage
      } else {
        return "text-error"; // Red text for low percentage
      }
    },
    // Global Stats Computed Properties
    currentQuestion() {
      return this.userStore.getReviewMode
        ? this.userStore.getCurrentlyReviewedQuestion
        : this.userStore.getCurrentQuestion;
    },
    currentQuestionId() {
      return this.currentQuestion ? this.currentQuestion.id : null;
    },
    questionStats() {
      return (
        this.questionStatsStore.getQuestionStatsById(
          this.currentQuestionId
        ) || {
          times_asked: 0,
          times_answered_correct: 0,
          times_skipped: 0,
          times_flagged: 0,
          times_answered: 0,
          times_upvoted: 0,
          times_downvoted: 0,
        }
      );
    },
    author() {
      return this.currentQuestion ? this.currentQuestion.author : null;
    },
    source() {
      return this.currentQuestion ? this.currentQuestion.source : null;
    },
    chapterId() {
      return this.currentQuestion ? this.currentQuestion.chapter_id : null;
    },
    chapter() {
      return this.userStore.getChapterById(this.chapterId);
    },
    correctPercentage() {
      const stats = this.questionStats;
      if (stats.times_answered > 0) {
        return (stats.times_answered_correct / stats.times_answered) * 100;
      } else {
        return 0;
      }
    },
    globalCircularColor() {
      const percentage = this.correctPercentage;
      if (percentage >= 60) {
        return "success"; // High percentage - green
      } else if (percentage >= 30) {
        return "warning"; // Medium percentage - yellow
      } else {
        return "error"; // Low percentage - red
      }
    },
    globalPercentageClass() {
      const percentage = this.correctPercentage;
      if (percentage >= 70) {
        return "text-success"; // Green text for high percentage
      } else if (percentage >= 40) {
        return "text-warning"; // Yellow text for medium percentage
      } else {
        return "text-error"; // Red text for low percentage
      }
    },
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

h3 {
  font-weight: 500;
  font-size: 1.2rem;
  color: #666;
}

.v-progress-circular {
  margin: 10px 0;
}
</style>
