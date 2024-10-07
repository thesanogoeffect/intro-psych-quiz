<template>
  <div>
    <NuxtPage />
  </div>
</template>

<script>
import { useQuestionStore } from "./stores/question";
export default {
  setup() {
    const questionStore = useQuestionStore();

    onMounted(async () => {
      await questionStore.setUp();
    });
  },
};
</script>
