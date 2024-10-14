import { useQuestionStatsStore } from "#imports";
export const useQuestionStore = defineStore("question", {
  state: () => ({
    total_shown_questions: 0,
    total_answered_questions: 0,
    total_correct_answers: 0,
    total_skipped_questions: 0,
    answerHistory: [], // Store the full question objects with guesses for easier UI display
    all_questions: [], // as loaded from JSON file, including all original data
    questionQueue: [], // queue holding the questions waiting to be asked

    currentQuestion: null, // the current question being asked
    skipsRemaining: 3, // number of skips remaining for the user
    selected_chapters: [],
    selected_sources: [],
    reviewMode: false,
  }),
  getters: {
    filteredQuestions:
      (state) =>
      (chapter_ids = [], sources = [], question_ids = []) => {
        let filtered = state.all_questions;

        // Apply chapter_ids filter if provided
        if (chapter_ids.length > 0) {
          filtered = filtered.filter((question) =>
            chapter_ids.includes(question.chapter_id)
          );
        }

        // Apply sources filter if provided
        if (sources.length > 0) {
          filtered = filtered.filter((question) =>
            sources.includes(question.source)
          );
        }

        // Apply question_ids filter if provided
        if (question_ids.length > 0) {
          filtered = filtered.filter((question) =>
            question_ids.includes(question.id)
          );
        }

        return filtered;
      },

    randomQuestions:
      (state) =>
      (chapter_ids = [], sources = [], question_ids = []) => {
        let filteredQuestions = state.filteredQuestions(
          chapter_ids,
          sources,
          question_ids
        );

        // Shuffle the filtered questions
        const shuffled = filteredQuestions.sort(() => 0.5 - Math.random());
        return shuffled;
      },

    getReviewMode: (state) => state.reviewMode,

    getAnswerHistory: (state) => state.answerHistory,

    getCurrentQuestion: (state) => state.currentQuestion,

    getSkipsRemaining: (state) => state.skipsRemaining,

    getTotalShownQuestions: (state) => state.total_shown_questions,

    getTotalAnsweredQuestions: (state) => state.total_answered_questions,

    getTotalCorrectAnswers: (state) => state.total_correct_answers,

    getFilteredByChapterAndSource: (state) => {
      return state.all_questions.filter(
        (question) =>
          state.selected_chapters.includes(question.chapter_id) &&
          state.selected_sources.includes(question.source)
      );
    },

    isQueueEmpty: (state) => state.questionQueue.length === 0,

    getTotalQuestions: (state) => state.all_questions.length,

    getAnsweredQuestions: (state) => state.answerHistory.length,

    getAnsweredCorrectlyPercentage: (state) => {
      if (state.total_answered_questions === 0) return 0;
      return (
        (state.total_correct_answers / state.total_answered_questions) * 100
      );
    },
  },

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
    incrementTotalSkippedQuestions() {
      this.total_skipped_questions++;
    },
    toggleReviewMode() {
      this.reviewMode = !this.reviewMode;
    },
    async loadQuestionsFromJSON() {
      try {
        const response = await fetch("/l3.json");
        if (!response.ok) {
          throw new Error("Failed to load questions from JSON file");
        }
        this.all_questions = await response.json();
      } catch (error) {
        console.error(error.message);
      }
    },

    async fill_filters_from_questions() {
      let chapters = new Set();
      let sources = new Set();
      this.all_questions.forEach((question) => {
        chapters.add(question.chapter_id);
        sources.add(question.source);
      });
      this.selected_chapters = Array.from(chapters);
      this.selected_sources = Array.from(sources);
    },
    async setUp() {
      await this.loadQuestionsFromJSON();

      // Check if all_questions is loaded
      console.log("All Questions:", this.all_questions);

      await this.fill_filters_from_questions();

      // Generate the initial queue
      await this.generateQueue(this.selected_chapters, this.selected_sources);
      // here, pop withou calling .getFromQueue
      this.currentQuestion = await this.getFromQueue(true);
    },
    async reSetUpAfterFiltersChange() {
      // Generate the initial queue
      await this.generateQueue(this.selected_chapters, this.selected_sources);
      // here, call .getFromQueue with blockAnalytics set to true
      this.currentQuestion = await this.getFromQueue(true);
    },
    async generateQueue(chapter_ids = [], sources = [], question_ids = []) {
      // Filter and randomize the questions to generate a queue
      this.questionQueue = this.randomQuestions(
        chapter_ids,
        sources,
        question_ids
      ).map((question) => {
        // Create the answers array
        const answers = [
          question.correct_answer,
          question.distractor_1,
          question.distractor_2,
          question.distractor_3,
        ];

        // Shuffle the answers array
        const shuffledAnswers = answers.sort(() => 0.5 - Math.random());

        // Find the index of the correct answer in the shuffled array
        const correctAnswerIndex = shuffledAnswers.indexOf(
          question.correct_answer
        );

        // Return the formatted question object
        return {
          id: question.id,
          question_title: question.question_title,
          answers: shuffledAnswers, // Shuffled answers
          chapter_id: question.chapter_id,
          correct_answer_index: correctAnswerIndex, // Index of the correct answer
          guessed_index: null,
          skipped: false,
          source: question.source,
          author: question.author,
        };
      });
    },
    async getFromQueue(blockAnalytics = false) {
      const questionStatsStore = useQuestionStatsStore();

      if (this.questionQueue.length === 0) {
        console.info("The question queue is empty! Refilling the queue...");

        // Await generateQueue to ensure it completes before proceeding
        await this.generateQueue(this.selected_chapters, this.selected_sources);

        if (this.questionQueue.length === 0) {
          console.error("No questions available after queue refill.");
          this.currentQuestion = null; // Set currentQuestion to null if no questions are available
          return null;
        }
      }

      if (this.currentQuestion && !blockAnalytics) {
        await questionStatsStore.incrementCurrentQuestionFields();
      }
      // Pop the first question from the queue and set it as the current question
      const nextQuestion = this.questionQueue.shift();
      await questionStatsStore.fetchQuestionStats(String(nextQuestion.id)); // TODO change later so that more than one question can be fetched at a time this.currentQuestion = nextQuestion;
      // now submit the stats for the previous question to Firestore

      questionStatsStore.resetIncrementFields();
      return nextQuestion;
    },
    async skipQuestion() {
      const questionStatsStore = useQuestionStatsStore();
      if (!this.currentQuestion) {
        console.error("No current question to skip.");
        return;
      }

      if (this.skipsRemaining <= 0) {
        console.error("No skips remaining.");
        return;
      }

      this.skipsRemaining -= 1;

      // Mark the current question as skipped
      this.currentQuestion.skipped = true;

      // Add the current question to answerHistory
      this.answerHistory.push(this.currentQuestion);

      questionStatsStore.incrementCurrentQuestionFields[ // increment for firestore purposes
        "total_times_skipped"
      ] = true;
      // Pop the next question and set it as the current question
      this.currentQuestion = await this.getFromQueue();

      // Increment counters
      this.incrementTotalSkippedQuestions();
    },
    async answerCurrentQuestion(guessed_index) {
      const questionStatsStore = useQuestionStatsStore();
      if (!this.currentQuestion) {
        console.error("No current question to answer.");
        return;
      }

      this.currentQuestion.guessed_index = guessed_index;
      this.currentQuestion.skipped = false;
      const isCorrect =
        guessed_index === this.currentQuestion.correct_answer_index;

      if (isCorrect) {
        questionStatsStore.current_question_increment_fields[
          "total_answered_correct"
        ] = true;
      }
      questionStatsStore.current_question_increment_fields[
        "times_answered"
      ] = true;

      console.log("User's answer index:", guessed_index);
      console.log(
        "Correct answer index:",
        this.currentQuestion.correct_answer_index
      );
      console.log(
        "User's answer:",
        this.currentQuestion.answers[guessed_index]
      );
      console.log("Was the user's answer correct?", isCorrect);

      // Add the current question to answerHistory
      this.answerHistory.push(this.currentQuestion);

      // Increment counters
      this.incrementTotalAnsweredQuestions();
      if (isCorrect) {
        this.incrementTotalCorrectAnswers();

        // Generate a random integer between 2 and 5
        const randomInt = Math.floor(Math.random() * (5 - 2 + 1)) + 2;

        // Add a skip based on the randomly generated number of correct answers
        if (this.total_correct_answers % randomInt === 0) {
          if (this.skipsRemaining < 3) {
            this.skipsRemaining += 1;
          }
        }
      }

      // Pop the next question and set it as the current question
      this.currentQuestion = await this.getFromQueue();
    },
  },
});
