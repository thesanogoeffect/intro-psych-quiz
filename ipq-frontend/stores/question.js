export const useQuestionStore = defineStore("question", {
    state: () => ({
      total_shown_questions: 0,
      total_answered_questions: 0,
      total_correct_answers: 0,
      answerHistory: [], // Store the full question objects with guesses for easier UI display
      all_questions: [], // as loaded from JSON file
      questionQueue: [], // queue holding the questions waiting to be asked
      
      currentQuestion: null, // the current question being asked
      skipsRemaining: 3, // number of skips remaining for the user
      selected_chapters: [],
      selected_sources: [],
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
          // Filter questions first based on chapter_ids, sources, and question_ids
          let filteredQuestions = state.filteredQuestions(
            chapter_ids,
            sources,
            question_ids
          );
  
          // Shuffle the filtered questions
          const shuffled = filteredQuestions.sort(() => 0.5 - Math.random());
          return shuffled; // Return all shuffled questions
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
      async loadQuestionsFromJSON() {
        // load questions from JSON file located in /public/l3.json
        const response = await fetch("/l3.json");
        const data = await response.json();
        if (!response.ok) {
          console.error("Failed to load questions from JSON file");
          return;
        }
        this.all_questions = data;
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
        await this.fill_filters_from_questions();
        this.generateQueue(this.selected_chapters, this.selected_sources);
        this.currentQuestion = this.popQuestion();
      },
      generateQueue(chapter_ids = [], sources = [], question_ids = []) {
        // Filter and randomize the questions to generate a queue
        this.questionQueue = this.randomQuestions(chapter_ids, sources, question_ids);
      },
      popQuestion() {
        if (this.questionQueue.length === 0) {
          console.info("The question queue is empty! Refilling the queue...");
          this.generateQueue(this.selected_chapters, this.selected_sources);
          if (this.questionQueue.length === 0) {
            console.error("No questions available after queue refill.");
            this.currentQuestion = null; // Set currentQuestion to null if no questions are available
            return null;
          }
        }
        
        // Pop the first question from the queue and set it as the current question
        const nextQuestion = this.questionQueue.shift();
        this.currentQuestion = nextQuestion;
        
        return nextQuestion;
      },
      addAnsweredQuestion(question, guess, skipped = false) {
        // Add the full question object to answerHistory
        this.answerHistory.push({ ...question, guess: guess, skipped: skipped });
      },
      skipQuestion() {
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
        this.addAnsweredQuestion(this.currentQuestion, null, true); // `true` indicates it was skipped
        
        // Pop the next question and set it as the current question
        this.currentQuestion = this.popQuestion();
      },
      answerCurrentQuestion(guess, isCorrect) {
        if (!this.currentQuestion) {
          console.error("No current question to answer.");
          return;
        }
        
        // Add the current question to answerHistory
        this.addAnsweredQuestion(this.currentQuestion, guess);
        
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
        this.currentQuestion = this.popQuestion();
      }
    },
  });
  