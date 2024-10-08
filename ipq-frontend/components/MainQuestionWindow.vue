<template>
  <GuessQuestionWindow></GuessQuestionWindow>

</template>

<script>
import { defineComponent, computed } from 'vue';
import { useQuestionStore } from '#imports';
import GuessQuestionWindow from './GuessQuestionWindow.vue';
import ReviewQuestionWindow from './ReviewQuestionWindow.vue';

export default defineComponent({
  name: 'MainQuestionWindow',
  components:{
    GuessQuestionWindow,
    ReviewQuestionWindow,
  },
  setup() {
    const questionStore = useQuestionStore();
    return {
      questionStore,
      GuessQuestionWindow,
      ReviewQuestionWindow,

    };
  },
});
</script>

<style scoped>
/* Add any custom styling if needed */
</style>
