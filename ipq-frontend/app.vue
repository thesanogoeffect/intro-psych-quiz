<template>
  <div>
    <!-- Your template content that might depend on the async operation -->
    <NuxtPage />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useQuestionStore } from "./stores/question";
import { useQuestionStatsStore } from '#imports';
const questionStore = useQuestionStore();
const questionStatsStore = useQuestionStatsStore();
await questionStore.setUp();


onMounted(() => {
  questionStatsStore.loadDownvoteCacheFromLocalStorage();
  questionStatsStore.loadUpvoteCacheFromLocalStorage();
  questionStatsStore.loadFlagCacheFromLocalStorage();
});


</script>
