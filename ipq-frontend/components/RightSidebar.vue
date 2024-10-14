<template>
    <div>
      ok
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useQuestionStore } from '#imports';
  import { useQuestionStatsStore } from '#imports';
  
  export default {
    name: 'RightSidebar',
    setup() {
      const questionData = ref([
        { id: 1, title: 'Question 1 Data' },
        { id: 2, title: 'Question 2 Data' },
      ]);
      const questionStore = useQuestionStore();
      return {questionStore };
    },
  };
  </script>
  
  <style scoped>
  .headline {
    font-weight: bold;
  }
  </style>