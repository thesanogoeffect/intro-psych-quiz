<template>
  <div class="about">
    <div class="links">
      <a
        href="https://www.buymeacoffee.com/thesanogoeffect"
        target="_blank"
      >
        <img
          src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png"
          alt="Buy Me A Coffee"
          class="icon"
        />
      </a>

      <a href="https://github.com/thesanogoeffect/intro-psych-quiz" target="_blank">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" class="icon" />
        View GitHub Repo
      </a>

      <a href="https://www.linkedin.com/in/jakubwerner" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" class="icon" />
        Connect on LinkedIn
      </a>
    </div>
    
    <h1>About</h1>
    <NuxtLink to="/">Back to Home</NuxtLink>
    <br />
    <p>Developed for TU/e with ❤️ by Jakub Werner</p>
    <p>
      Thanks to prof. Daniël Lakens for endorsing the idea, also special thanks
      to Tim and Aaravee.
    </p>
    <p>
      This is currently not an official part of the TU/e course, just a passion
      project because I really like it. I am not responsible for any mistakes or inaccuracies.
    </p>
    <p>
      If you want to support the project: I am looking for people who have good grades
      in the course and can help me review the flagged questions.
      Feel free to contact me if you're interested.

      If you also like web design (even if you know little, you know more than me :D) and want to help me with the UI, that would be great!

    </p>
    <h2>F.A.Q.:</h2>
    <p><strong>What exactly is this and why does it exist?</strong></p>
    <p>
      I wanted to create a resource for fellow P&T students after seeing the
      previous years' students submitted questions. The idea was great, but
      sometimes there were mistakes in the questions, or they were not really
      good. Having a platform with a voting system and verified questions (at
      least by an LLM) seemed like a nice idea! I hope you find it useful. The
      quiz is just because it's fun :)
    </p>

    <p><strong>Can I upload my questions?</strong></p>
    <p>
      Unfortunately not at this time, because of a potential interference with
      the current course format.
    </p>

    <p><strong>What did it cost to make the app, and how did you pay for the hosting?</strong></p>
    <p>
      Nothing so far! Thanks to Vuetify, the generous Firebase free tier, and
      GitHub Pages & GitHub Actions! I only pay for the OpenAI tokens. If you
      like the project and want to attempt something similar yourself, feel free
      to contact me. In case you're also a student, check out the GitHub Student Pack!
    </p>

    <p><strong>How can I contact you?</strong></p>
    <p>
      For any questions or suggestions, hit me up at
      jakubwerner1@gmail.com or WhatsApp. I have already implemented some of
      your suggestions, thanks for that!
    </p>

    <p><strong>Did you steal the Reddit karma UI?</strong></p>
    <p>If you're from the Reddit legal team, then no, I did not</p>
  </div>
</template>

<script>
export default {
  name: "About",
};
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
  margin-bottom: 15px;
}

.about h2 {
  margin-top: 20px;
  margin-bottom: 10px;
}

.links {
  margin-bottom: 20px;
  display: flex;
  align-items: center; /* Aligns items vertically */
}

.links a {
  display: flex;
  align-items: center;
  margin-right: 15px;
  text-decoration: none;
  font-size: 1.1em;
}

.icon {
  width: 30px;
  height: 30px;
  margin-right: 8px;
  vertical-align: middle;
}

.links img.icon {
  width: auto;
  height: 60px; /* Matches the height of the Buy Me A Coffee button */
}
</style>