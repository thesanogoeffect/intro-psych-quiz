<template>
  <v-card class="rounded-pill pa-2" elevation="3" outlined>
    <!-- Upvote Button -->
    <v-btn
      :icon="upvoted ? 'mdi-arrow-up-bold' : 'mdi-arrow-up-bold-outline'"
      variant="plain"
      v-ripple
      class="mx-2 upvote-button"
      @click="handleUpvote"
      :color="upvoted? 'success' : ''"
      :class="{ voted: upvoted }"
    ></v-btn>

    <!-- Karma Display -->
    <v-chip class="rounded-pill" color="grey lighten-3">
      <v-avatar>
        <v-icon>mdi-karma</v-icon>
      </v-avatar>
      <!-- Conditionally set the color of the karma number -->
      <span
        :style="{
          color: karma> 0 ? '#4CAF50' : karma < 0 ? '#F44336' : '',
        }"
        >{{ karma }}</span
      >
    </v-chip>

    <!-- Downvote Button -->
    <v-btn
      :icon="
        downvoted? 'mdi-arrow-down-bold' : 'mdi-arrow-down-bold-outline'
      "
      variant="plain"
      v-ripple
      class="mx-2"
      @click="handleDownvote"
      :color="downvoted ? 'error' : ''"
      :class="{ voted: downvoted}"
    ></v-btn>

    <!-- Flag Button -->
    <v-btn
      :icon="flagged ? 'mdi-flag' : 'mdi-flag-outline'"
      variant="plain"
      v-ripple
      class="mx-2"
      @click="toggleFlagged"
      :class="{ flagged: flagged }"
    ></v-btn>
  </v-card>
</template>

<script setup>
import { ref, computed } from "vue";
import { useQuestionStatsStore } from "#imports";
import { useQuestionStore } from "#imports";
import { useDisplay } from "#imports";

// Initialize the store
const questionStatsStore = useQuestionStatsStore();
const questionStore = useQuestionStore();
const display = useDisplay();

// Computed properties
const mdAndUp = computed(() => display.mdAndUp);


const currentQuestion = computed(() => {
  return questionStore.getReviewMode
    ? questionStore.getCurrentlyReviewedQuestion
    : questionStore.getCurrentQuestion;
});
const currentQuestionId = computed(() => currentQuestion.value.id);
const statsCache = computed(() =>
  questionStatsStore.getQuestionStatsById(currentQuestionId.value)
);
const upvoted = computed(() =>
  questionStatsStore.getUpvoteCacheById(currentQuestionId.value)
);
const downvoted = computed(() =>
  questionStatsStore.getDownvoteCacheById(currentQuestionId.value)
);
const flagged = computed(() =>
  questionStatsStore.getFlagCacheById(currentQuestionId.value)
);
const karma = computed(
  () => statsCache.value.times_upvoted - statsCache.value.times_downvoted
);

// Handle upvote logic
const handleUpvote = () => {
    if (upvoted.value) {
        questionStatsStore.cancelUpvoteSpecificQuestion(currentQuestionId.value);
    } else {
        questionStatsStore.upvoteSpecificQuestion(currentQuestionId.value);
    }
};

// Handle downvote logic
const handleDownvote = () => {
  if (downvoted.value) {
    questionStatsStore.cancelDownvoteSpecificQuestion(currentQuestionId.value);
  } else {
    questionStatsStore.downvoteSpecificQuestion(currentQuestionId.value);
  }
};

// Toggle flagged state
const toggleFlagged = () => {
    console.log("toggleFlagged");
    console.log(flagged.value);
  if (flagged.value) {
    questionStatsStore.cancelFlagSpecificQuestion(currentQuestionId.value);
  } else {
    questionStatsStore.flagSpecificQuestion(currentQuestionId.value);
  }
};
</script>

<style scoped>
.rounded-pill {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.v-btn {
  transition: transform 0.2s ease-in-out;
}

.v-btn.voted {
  transform: scale(1.2);
}

.v-btn.flagged {
  color: red;
}
</style>
