    <template>
        <v-app>
            <v-card>
                <v-layout>
                    <!-- App Bar -->
                    <v-app-bar color="primary" prominent>
                        <v-app-bar-nav-icon
                            variant="text"
                            @click.stop="drawer = !drawer"
                        ></v-app-bar-nav-icon>

                        <v-toolbar-title class="app_title">Intro to Psychology Quiz</v-toolbar-title>

                        <v-spacer></v-spacer>

                        <template v-if="$vuetify.display.mdAndUp">
                            <v-btn icon="mdi-filter" variant="text"></v-btn>
                        </template>
                        <v-btn icon="mdi-"
                        <v-btn icon="mdi-information-box" variant="text"></v-btn>
                    </v-app-bar>

                    <v-navigation-drawer
                        v-model="drawer"
                        permanent
                    >
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
        data() {
            return {
                drawer: true,
            };
        },
        setup() {
            const questionStore = useQuestionStore();
            function darkMode() {
            this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
            },
            return {
                questionStore,
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
