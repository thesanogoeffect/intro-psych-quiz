    <template>
  <v-app>
    <v-card>
      <v-layout>
        <!-- App Bar -->
        <v-app-bar color="primary" prominent>
          <v-app-bar-nav-icon
            variant="text"
            @click.stop="drawer = !drawer"
            icon="mdi-chart-bar"
          ></v-app-bar-nav-icon>

          <v-toolbar-title class="app_title"
            >Intro to Psychology Quiz</v-toolbar-title
          >

          <v-spacer></v-spacer>

          <template v-if="$vuetify.display.mdAndUp">
            <v-btn icon="mdi-filter" variant="text"></v-btn>
          </template>
          <v-btn icon="mdi-theme-light-dark" @click="toggleTheme"></v-btn>
          <v-btn icon="mdi-information" variant="text" @click="routeToAbout"></v-btn>
        </v-app-bar>

        <v-navigation-drawer v-model="drawer" permanent >
          <LeftSidebar />
        </v-navigation-drawer>
        <v-main style="height: 700px; width: 200px">
          <MainQuestionWindow />
        </v-main>
      </v-layout>
    </v-card>
  </v-app>
</template>

<script>
import LeftSidebar from "~/components/LeftSidebar.vue";

export default {
  name: "Home",
  components: {
    LeftSidebar,
  },
  setup() {
    const questionStore = useQuestionStore();
    const drawer = ref(true); // Reactive state for the drawer
    const router = useRouter();
    const theme = useTheme();

    function toggleTheme() {
      theme.global.name.value = theme.global.name.value === 'light' ? 'dark' : 'light'
    }
    const routeToAbout = () => {
        router.push({ path: '/about' });
    };

    return {
      questionStore,
      drawer,
      routeToAbout,
      toggleTheme,
    };
  },
};
</script>
    <style scoped>
h1 {
  color: #42b983;
}
.app_title {
  color: white;
}
</style>
