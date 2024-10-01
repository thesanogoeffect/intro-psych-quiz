**Plans for development:**

Having multiple databases

L1 - all obtained questions, including source (Google Form? Previous year's? Google Doc? OpenStax?), author, email, date,...
L2 - all questions with check data - is_format_valid? is_correct_chapter? is_question_correct? is_sufficient?
L3 - only verified, valid questions including all metadata (correct formatting, grammar, chapter).
L4 - questions enriched by quality ratings (user-ratings, LLM ratings)
L5 - final set for student practice, only questions above a certain quality score

On question submit pipeline using LLMs
step 1: verify valid format (has 4 different answers? makes gene