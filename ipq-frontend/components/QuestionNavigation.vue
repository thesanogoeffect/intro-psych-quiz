<template>
  <v-container class="d-flex justify-center">
    <v-btn
      icon="mdi-arrow-left"
      :disabled="!canGoLeft"
      @click="useLeftArrow"
    >
    </v-btn>
    <v-btn
      icon="mdi-arrow-right"
      :disabled="!canGoRight"
      @click="useRightArrow"
    >
    </v-btn>
  </v-container>
</template>

<script setup>
import { useQuestionStore } from "#imports";
import { ref, onMounted, onBeforeUnmount, computed } from "vue";

const questionStore = useQuestionStore();
const clickBlocked = ref(false); // Flag to block clicks

const canGoLeft = computed(() => {
  if (questionStore.getReviewMode) {
    return questionStore.getCurrentReviewPosition > 0;
  } else {
    return questionStore.getAnswerHistoryLength > 0;
  }
});

const canGoRight = computed(() => {
  return questionStore.getReviewMode
    ? true
    : questionStore.getSkipsRemaining > 0;
});

function blockClickTemporarily() {
  clickBlocked.value = true;
  setTimeout(() => {
    clickBlocked.value = false;
  }, 400); 
}

function useLeftArrow() {
  if (clickBlocked.value) return; // Prevent action if click is blocked
  blockClickTemporarily();

  if (questionStore.getReviewMode) {
    if (questionStore.getCurrentReviewPosition > 0) {
      questionStore.previousReviewedQuestion();
    }
  } else {
    questionStore.toggleReviewMode();
  }
}

function useRightArrow() {
  if (clickBlocked.value) return; // Prevent action if click is blocked
  blockClickTemporarily();

  if (questionStore.getReviewMode) {
    if (questionStore.getCurrentReviewPosition === questionStore.getAnswerHistoryLength - 1) {
      questionStore.toggleReviewMode();
    } else {
      questionStore.nextReviewedQuestion();
    }
  } else {
    questionStore.skipQuestion();
  }
}

// Handle arrow key presses
function handleKeydown(event) {
  if ((event.key === 'ArrowLeft' || event.key === 'a' || event.key === 'A') && canGoLeft.value) {
    event.preventDefault(); // prevent default arrow key behavior
    useLeftArrow();
  } else if ((event.key === 'ArrowRight' || event.key === 'd' || event.key === 'D') && canGoRight.value) {
    event.preventDefault(); // prevent default arrow key behavior
    useRightArrow();
  }
}

// Mount the keydown event listener
onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
});

// Remove the keydown event listener when the component is unmounted
onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown);
});
</script>