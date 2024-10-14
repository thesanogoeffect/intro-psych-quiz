<template>
  <v-container v-if="isStoreInitialized" class="py-3">
    <v-row>
      <v-col>
        <div class="stats-container pa-3">
          <h2 class="mb-2">Stats</h2>
          <h3 class="mb-3">Overview</h3>
          <v-row>
            <v-col>
              <v-icon color="secondary">mdi-eye-outline</v-icon>
              Total Shown: {{ userStore.getTotalShownQuestions }}
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-icon color="primary"
                >mdi-checkbox-marked-circle-outline</v-icon
              >
              Answered: {{ userStore.getTotalAnsweredQuestions }}
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-icon color="success">mdi-check-circle-outline</v-icon>
              Correct: {{ userStore.getTotalCorrectAnswers }}
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-icon color="warning">mdi-skip-next-circle-outline</v-icon>
              Skipped: {{ userStore.getSkippedQuestions }}
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-icon color="info">mdi-help-circle-outline</v-icon>
              Skips Left: {{ userStore.getSkipsRemaining }}
            </v-col>
          </v-row>
          <v-row v-show="userStore.getTotalAnsweredQuestions > 0" justify="center">
            <v-col cols="12" class="text-center">
              <v-progress-circular
                :model-value="userStore.getAnsweredCorrectlyPercentage"
                :color="circularColor"
                size="78"
                width="10"
              >
                <span :class="percentageClass">{{ formattedPercentage }}%</span>
              </v-progress-circular>
              <div>Correct Percentage</div>
            </v-col>
          </v-row>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useQuestionStore } from "#imports"; // Ensure correct store import

export default {
  data() {
    return {
      isStoreInitialized: false,
      userStore: null,
    };
  },
  created() {
    try {
      this.userStore = useQuestionStore();
      this.isStoreInitialized = true;
    } catch (error) {
      console.error("Pinia store is not initialized:", error);
    }
  },
  computed: {
    formattedPercentage() {
      return this.userStore.getAnsweredCorrectlyPercentage.toFixed(1);
    },
    circularColor() {
      const percentage = this.userStore.getAnsweredCorrectlyPercentage;
      if (percentage >= 70) {
        return "success"; // High percentage - green
      } else if (percentage >= 40) {
        return "warning"; // Medium percentage - yellow
      } else {
        return "error"; // Low percentage - red
      }
    },
    percentageClass() {
      const percentage = this.userStore.getAnsweredCorrectlyPercentage;
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
