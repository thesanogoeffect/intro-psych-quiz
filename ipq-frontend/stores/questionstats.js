import { defineStore } from "pinia";
import { getQuestionById, incrementQuestionFields } from "~/services/firestore";
// THIS STORE IS ONLY FOR DATA THAT GOES TO FIRESTORE!

// This store enables us to access the Firestore data easily
// It will have a function that will fetch the data from Firestore based on the question_id
// Also increment functions for the question_id

export const useQuestionStatsStore = defineStore("questionstats", {
  state: () => ({
    current_question_stats: null, // a dictionary, as retrieved from Firestore or cache
    current_question_id: null,
    question_cache: {}, // a dictionary of question_id to question_stats
    // the following keep track whether the user has upvoted, downvoted, flagged etc.
    upvote_cache: {}, // a dictionary of question_id to true/false
    downvote_cache: {}, // a dictionary of question_id to true/false
    // a dictionary of question_id to true/false
    flag_cache: {}, // a dictionary of question_id to true/false

    current_questions_increment_fields: {}, // {int: dict} a dictionary of question_id to fields to increment, current proposed changes
    cached_questions_increment_fields: {}, // keeping track of what was already sent to Firestore

    new_question_increment_fields: {
      times_asked: false,
      times_answered_correct: false,
      times_skipped: false,
      times_flagged: false,
      times_answered: false,
      times_upvoted: false,
      times_downvoted: false,
    }, // a dictionary of fields to increment
  }),

  getters: {
    // Get the stats for the current question
    currentQuestionStats: (state) => {
      return state.current_question_stats;
    },
    getQuestionStatsById: (state) => (question_id) => {
      return state.question_cache[question_id];
    },
    getCurrentIncrementFieldsbyId: (state) => (question_id) => {
      return state.current_questions_increment_fields[question_id] || {};
    },
    getCachedIncrementFieldsbyId: (state) => (question_id) => {
      return state.cached_questions_increment_fields[question_id] || {};
    },
    getUpvoteCache: (state) => {
      return state.upvote_cache;
    },
    getDownvoteCache: (state) => {
      return state.downvote_cache;
    },
    getFlagCache: (state) => {
      return state.flag_cache;
    },
    getUpvoteCacheById: (state) => (question_id) => {
      return state.upvote_cache[question_id];
    },
    getDownvoteCacheById: (state) => (question_id) => {
      return state.downvote_cache[question_id];
    },
    getFlagCacheById: (state) => (question_id) => {
      return state.flag_cache[question_id];
    },
  },

  actions: {
    async fetchQuestionStats(question_id) {
      // Fetch question stats from Firestore
      this.current_question_id = question_id;
      // Now fetch the dict based on question_id from Firestore, if not in cache
      if (question_id in this.question_cache) {
        this.current_question_stats = this.getQuestionStatsById(question_id);
        console.log("Fetched from cache");
        return;
      }
      this.current_question_stats = await getQuestionById(question_id);
      // save to cache
      this.question_cache[question_id] = { ...this.current_question_stats };

      //generate upvote, downvote and flag cache
      this.upvote_cache[question_id] = false;
      this.downvote_cache[question_id] = false;
      this.flag_cache[question_id] = false;

      // generate the increment fields
      await this.preBuildIncrementFields([question_id]);
    },

    async batchFetchQuestionStats(question_ids) {
      // Fetch question stats from Firestore
      for (const question_id of question_ids) {
        await this.fetchQuestionStats(question_id);
      }
    },
    async incrementSpecificQuestionFields(question_id) {
      // yeet into Firestore
      // get the current proposed changes to Firestore
      const fields = this.getCurrentIncrementFieldsbyId(question_id);
      // look to see if the fields were already sent to Firestore
      const cached_fields = this.getCachedIncrementFieldsbyId(question_id);
      // console.log("Incrementing fields for question_id: " + question_id);
      // get only the key: value pairs that differ from the cached fields
      const fields_to_increment = [];
      const fields_to_decrement = [];
      for (const [key, value] of Object.entries(fields)) {
        if (value != cached_fields[key]) {
          if (value) {
            fields_to_increment.push(key);
            this.question_cache[question_id][key] += 1;
          } else if (!value) {
            fields_to_decrement.push(key);
            this.question_cache[question_id][key] -= 1;
          }
        }
      }
      // now also update the cache
      // for the false values, decrement the fields
      // for the true values, increment the fields
      // process the increment fields in Firestore
      await incrementQuestionFields(question_id, fields_to_increment, false);
      await incrementQuestionFields(question_id, fields_to_decrement, true);
      // update the cache
      this.cached_questions_increment_fields[question_id] = { ...fields };

    },
    upvoteSpecificQuestion(question_id) {
      // Upvote the selected question in retrospect
      this.upvote_cache[question_id] = true;
      this.current_questions_increment_fields[question_id]["times_upvoted"] = true;
      if (this.getDownvoteCacheById(question_id)) {
        this.cancelDownvoteSpecificQuestion(question_id);
      }
    },
    downvoteSpecificQuestion(question_id) {
      // Downvote the selected question in retrospect
      this.downvote_cache[question_id] = true;
      this.current_questions_increment_fields[question_id]["times_downvoted"] = true;
      if (this.getUpvoteCacheById(question_id)) {
        this.cancelUpvoteSpecificQuestion(question_id);
      }

    },
    flagSpecificQuestion(question_id) {
      // Flag the selected question in retrospect
      this.flag_cache[question_id] = true;
      this.current_questions_increment_fields[question_id]["times_flagged"] = true;

    },
    cancelUpvoteSpecificQuestion(question_id) {
      // Deupvote the selected question in retrospect
      this.upvote_cache[question_id] = false;
      this.current_questions_increment_fields[question_id]["times_upvoted"] = false;

    },
    cancelDownvoteSpecificQuestion(question_id) {
      // Dedownvote the selected question in retrospect
      this.downvote_cache[question_id] = false;
      this.current_questions_increment_fields[question_id]["times_downvoted"] = false;

    },
    cancelFlagSpecificQuestion(question_id) {
      // Deflag the selected question in retrospect
      this.flag_cache[question_id] = false;
      this.current_questions_increment_fields[question_id]["times_flagged"] = false;

    },
    // reset current_question_increment_fields

    async preBuildIncrementFields(ids) {
      // populate the current_questions_increment_fields and cached_questions_increment_fields with new_question_increment_fields
      for (const id of ids) {
        this.current_questions_increment_fields[id] = { ...this.new_question_increment_fields };
        this.cached_questions_increment_fields[id] = { ...this.new_question_increment_fields };
      }
    }

  },
});
