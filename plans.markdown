**Plans for development:**

Having multiple databases

L1 - all obtained questions, including source (Google Form? Previous year's? Google Doc? OpenStax?), author, email, date,...
L2 - all questions with check data - is_format_valid? is_correct_chapter? is_question_correct? is_sufficient?
L3 - only verified, valid questions including all metadata (correct formatting, grammar, chapter).
L4 - questions enriched by quality ratings (user-ratings, LLM ratings)
L5 - final set for student practice, only questions above a certain quality score

On question submit pipeline using LLMs
step 1: verify valid format (has 4 different answers? makes general sense?)
    if not:
        discard, fix if fixable
    step 2: is the question related to the supposed chapter?
        if not:
            reassign if related to another, else discard
        step 3: is it a good question?
            if not:
                fix if can be fixed

Duplicate check
1: is a question a direct duplicate of another?
    if yes:

Adding a report question form!
Adding question 5-star review system after the user answers, so that we get quality data

**Ideas**
Make Google Doc read-only, because of low crowd-source
Yoink mechanism for DL