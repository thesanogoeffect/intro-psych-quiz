import { defineStore } from "pinia";
import { getQuestionById, incrementQuestionFields } from "~/services/firestore";

// This store enables us to access the Firestore data easily
// It will have a function that will fetch the data from Firestore based on the question_id
// Also increment functions for the question_id

export const useQuestionStatsStore = defineStore("questionstats", {
  state: () => ({
    current_question_stats: null, // a dictionary, as retrieved from Firestore or cache
    current_question_id: null,
    question_cache: {}, // a dictionary of question_id to question_stats
    // the following keep track whether the user has upvoted, downvoted, flagged etc.
    upvote_cache: {},  // a dictionary of question_id to true/false
    downvote_cache: {}, // a dictionary of question_id to true/false
    flag_cache: {}, // a dictionary of question_id to true/false

    current_question_increment_fields: {
      times_got_asked: true,
      total_answered_correct: false,
      total_times_skipped: false,
      times_flagged: false,
      total_answered: false,
      times_upvoted: false,
      times_downvoted: false,
    }, // a dictionary of fields to increment
  }),

  getters: {
    // Get the stats for the current question
    currentQuestionStats: (state) => {
      return state.current_question_stats;
    },
  },

  actions: {
    async fetchQuestionStats(question_id) {
      // Fetch question stats from Firestore
      this.current_question_id = question_id;
      // Now fetch the dict based on question_id from Firestore, if not in cache
      if (question_id in this.question_cache) {
        this.current_question_stats = this.question_cache[question_id];
        console.log("Fetched from cache");
        console.log(this.current_question_stats);
        return;
      }
      this.current_question_stats = await getQuestionById(question_id);
      console.log(this.current_question_stats);
      // save to cache
      this.question_cache[question_id] = this.current_question_stats;
    },

    async batchFetchQuestionStats(question_ids) {
      // Fetch question stats from Firestore
      for (const question_id of question_ids) {
        await this.fetchQuestionStats(question_id);
      }
    },
    async incrementCurrentQuestionFields() {
      // Increment the fields of the current question, that are set to true in the current_question_increment_fields dictionary
      // go through the dictionary and generate an array of fields to increment
      const fields_to_increment_array = [];
      for (const field in this.current_question_increment_fields) {
        if (this.current_question_increment_fields[field]) {
          fields_to_increment_array.push(field);
        }
      }
      console.log(
        "Incrementing fields for question_id:",
        this.current_question_id
      );
      console.log(fields_to_increment_array);
      // increment the fields
      await incrementQuestionFields(
        this.current_question_id,
        fields_to_increment_array
      );
    },
    upvoteCurrentQuestion() {
      // Upvote the current question
      this.current_question_increment_fields["times_upvoted"] = true;
      this.current_question_increment_fields["times_downvoted"] = false;
      this.upvote_cache[this.current_question_id] = true;
      this.downvote_cache[this.current_question_id] = false;
    },
    downvoteCurrentQuestion() {
      // Downvote the current question
      this.current_question_increment_fields["times_downvoted"] = true;
      this.current_question_increment_fields["times_upvoted"] = false;
      this.downvote_cache[this.current_question_id] = true;
        this.upvote_cache[this.current_question_id] = false;
    },
    flagCurrentQuestion() {
      // Flag the current question
      this.current_question_increment_fields["times_flagged"] = true;
      this.flag_cache[this.current_question_id] = true;
    },
    canceUpvoteCurrentQuestion() {
      // Deupvote the current question
      this.current_question_increment_fields["times_upvoted"] = false;
      this.upvote_cache[this.current_question_id] = false;
    },
    cancelDownvoteCurrentQuestion() {
      // Dedownvote the current question
      this.current_question_increment_fields["times_downvoted"] = false;
      this.downvote_cache[this.current_question_id] = false;
    },
    cancelFlagCurrentQuestion() {
      // Deflag the current question
      this.current_question_increment_fields["times_flagged"] = false;
      this.flag_cache[this.current_question_id] = false;
    },
    upvotePreviousQuestion(question_id) {
      // Upvote the selected question in retrospect
      this.upvote_cache[question_id] = true;
      this.downvote_cache[question_id] = false;
      incrementQuestionFields(question_id, ["times_upvoted"], false);
      incrementQuestionFields(question_id, ["times_downvoted"], true);
    },
    downvotePreviousQuestion(question_id) {
      // Downvote the selected question in retrospect
      this.downvote_cache[question_id] = true;
      this.upvote_cache[question_id] = false;
      incrementQuestionFields(question_id, ["times_downvoted"], false);
      incrementQuestionFields(question_id, ["times_upvoted"], true);
    },
    flagPreviousQuestion(question_id) {
      // Flag the selected question in retrospect
      this.flag_cache[question_id] = true;
      incrementQuestionFields(question_id, ["times_flagged"]);
    },
    cancelUpvotePreviousQuestion(question_id) {
      // Deupvote the selected question in retrospect
      this.upvote_cache[question_id] = false;
      incrementQuestionFields(question_id, ["times_upvoted"], true);
    },
    cancelDownvotePreviousQuestion(question_id) {
      // Dedownvote the selected question in retrospect
      this.downvote_cache[question_id] = false;
      incrementQuestionFields(question_id, ["times_downvoted"], true);
    },
    cancelFlagPreviousQuestion(question_id) {
      // Deflag the selected question in retrospect
      this.flag_cache[question_id] = false;
      incrementQuestionFields(question_id, ["times_flagged"], true);
    },
    // reset current_question_increment_fields
    resetIncrementFields() {
      this.current_question_increment_fields = {
        times_got_asked: true,
        total_answered_correct: false,
        total_times_skipped: false,
        times_flagged: false,
        total_answered: false,
        times_upvoted: false,
        times_downvoted: false,
      };
    },
  },
});
