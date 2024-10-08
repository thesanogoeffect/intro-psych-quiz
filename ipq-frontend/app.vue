<template>
  <div>
    <!-- Your template content that might depend on the async operation -->
    <NuxtPage />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useQuestionStore } from "./stores/question";
const questionStore = useQuestionStore();
await questionStore.setUp();

</script>
