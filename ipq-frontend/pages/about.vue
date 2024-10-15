<template>
    <div class="about">
        <h1>About</h1>
        <NuxtLink to="/">Back to Home</NuxtLink>
        <br><p>Developed for TU/e with ❤️ by Jakub Werner</p>
        <p>Thanks to Daniël Lakens for endorsing the idea, also special thanks to Tim, Aaravee, Suri, Eme. </p>


        <p><i>Pro tip - you can use A+D or Arrow keys to cycle between the questions!</i></p>
        <h2>F.A.Q.:</h2>
        <p><strong>What exactly is this and why does it exist?</strong></p>
        <p>I wanted to create a resource for fellow P&T students after seeing the prev years' students submitted questions. The idea was great, but sometimes there were mistakes in the questions, or they were not really good.
            Having a platform with a voting system and verified questions (at least by an LLM) seemed like a nice idea! I hope you find it useful. The quiz is just because it's fun :)
        </p>

        <p><strong>Can I upload my questions?</strong></p>
        <p>Unfortunately not at this time, because of a potential interference with the current course format.</p>

        <p><strong>What did it cost to make the app, how did you pay for the hosting?</strong></p>
        <p> Nothing so far! Thanks to Vuetify, the generous Firebase free tier and the GitHub Student Pack. Check them out!
            I only pay for the OpenAI tokens, but with new GPT-4o mini, costs are practically nonexistent. If you like the project and want to attempt something similar yourself, feel free to contact me </p>
        
            <p><strong>How can I contact you?</strong></p>
        <p>For any questions or suggestions, hit me up at jakubwerner1@gmail.com or WhatsApp. I have already implemented some of your them, thanks for that!</p>

        <p><strong>Did you steal the Reddit karma UI?</strong></p>
        <p>If you're from the Reddit legal team, then no, I did not</p>

        <p><strong>Why does this look like it was mostly written by ChatGPT?</strong></p>
        <p>Because...it was</p>
    </div>
</template>

<script>
export default {
    name: 'About'
}
</script>

<style scoped>
.about {
    padding: 20px;
}

.about h1 {
    font-size: 2em;
    margin-bottom: 10px;
}

.about p {
    font-size: 1.2em;
    margin-bottom: 15px; /* Added more spacing between paragraphs */
}

.about h2 {
    margin-top: 20px;
    margin-bottom: 10px;
}
</style>