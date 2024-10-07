
export const useStatsStore = defineStore("stats", {
  state: () => ({
    total_shown_questions: 0,
    total_answered_questions: 0,
    total_correct_answers: 0,
    // guess is 
  }),
  actions: {
    incrementTotalShownQuestions() {
      this.total_shown_questions++;
    },
    incrementTotalAnsweredQuestions() {
      this.total_answered_questions++;
    },
    incrementTotalCorrectAnswers() {
      this.total_correct_answers++;
    },
  },
});
