import { defineStore } from "pinia";
import { onMounted } from "vue"
const { $questionsRef } = useNuxtApp();
onMounted(() => console.log($questionsRef))
// this store enables us to access the firestore data easily
// will have a function that will fetch the data from firestore based on the question_id
// also increment functions for the question_id
//const models = useCollection($modelsRef);

export const useQuestionStatsStore = defineStore("questionstats", {
    state: () => ({
        current_question_stats : null, // a dictionary
        question_id : null,
        question_cache : null // a dictionary of question_id to question_stats
    }),

    actions: {
        async fetchQuestionStats(question_id) {
            
}
    