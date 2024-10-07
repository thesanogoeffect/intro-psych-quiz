<template>
    <div>
        <p>Enable review mode?</p>
      <ToggleSwitch v-model="guessToggle" />
      <GuessQuestionWindow v-if="!reviewMode" v-model="reviewMode"></GuessQuestionWindow>
      <ReviewQuestionWindow v-else v-model="review_mode"></ReviewQuestionWindow>

    </div>
  </template>
  
  <script>
  import { ref, watch } from "vue";
  import ToggleSwitch from "primevue/toggleswitch";
  import GuessQuestionWindow from "@/components/GuessQuestionWindow";
  import ReviewQuestionWindow from "@/components/ReviewQuestionWindow";
  import { useQuestionStore } from "#imports";
  
  export default {
    name: "MainQuestionWindow",
    components: {
      GuessQuestionWindow,
      ReviewQuestionWindow,
      ToggleSwitch,
    },
    setup() {
      // Reactive state
      const reviewMode = ref(false);
      const guessToggle = ref(true);

      const questionStore = useQuestionStore();

  
      // Watch the reviewToggle and update reviewMode accordingly
      watch(guessToggle, (newValue) => {
        if (!reviewMode.value) {
          reviewMode.value = !newValue;
        }
      });
  
      return {
        reviewMode,
        guessToggle,
        questionStore,
      };
    },
  };
  </script>
  
  <style scoped>
  </style>
  