<template>
  <v-app>
    <v-card>
      <v-layout column fill-height>
        <!-- App Bar -->
        <v-app-bar color="primary" prominent>
          <v-app-bar-nav-icon
            variant="text"
            @click="drawer = !drawer"
            icon="mdi-chart-bar"
          ></v-app-bar-nav-icon>

          <v-toolbar-title class="app_title">
            Intro to Psychology Quiz
          </v-toolbar-title>

          <v-spacer></v-spacer>

          <v-btn
            icon="mdi-filter"
            variant="text"
            @click="filterDialog = true"
          ></v-btn>
          <v-btn icon="mdi-theme-light-dark" @click="toggleTheme"></v-btn>
          <v-btn
            icon="mdi-information"
            variant="text"
            @click="routeToAbout"
          ></v-btn>
        </v-app-bar>

        <!-- Left Navigation Drawer -->
        <v-navigation-drawer v-model="drawer" location="left" v-if="drawer">
          <LeftSidebar />
        </v-navigation-drawer>

        <!-- Right Navigation Drawer (RightSidebar) -->
        <v-navigation-drawer location="right">
          <RightSidebar />
        </v-navigation-drawer>

        <v-container fluid fill-height>
          <v-main>
            <MainQuestionWindow />
          </v-main>
        </v-container>
      </v-layout>

      <v-dialog v-model="filterDialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span class="headline">Filter Questions</span>
          </v-card-title>

          <v-card-text>
            <!-- Chapter Selection -->
            <v-select
              multiple
              variant="solo"
              :items="availableChapters"
              v-model="selectedChapters"
              label="Select Chapter"
            ></v-select>
            <v-btn text @click="selectAllChapters">Select All Chapters</v-btn>
            <v-btn text @click="deselectAllChapters"
              >Deselect All Chapters</v-btn
            ><br />

            <!-- Source Selection -->
            <v-select
              multiple
              variant="solo"
              :items="availableSources"
              v-model="selectedSources"
              label="Select Source"
            ></v-select>
            <v-btn text @click="selectAllSources">Select All Sources</v-btn>
            <v-btn text @click="deselectAllSources">Deselect All Sources</v-btn>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="filterDialog = false">Cancel</v-btn>
            <v-btn :disabled="!canApplyFilters" text @click="applyFilters"
              >Apply</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
  </v-app>
</template>

<script>
import { ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useTheme } from "vuetify";
import LeftSidebar from "~/components/LeftSidebar.vue";
import MainQuestionWindow from "~/components/MainQuestionWindow.vue";
import RightSidebar from "~/components/RightSidebar.vue";
import { useQuestionStore } from "#imports";

export default {
  name: "Home",
  components: {
    LeftSidebar,
    MainQuestionWindow,
    RightSidebar,
  },
  setup() {
    const drawer = ref(true);
    const router = useRouter();
    const theme = useTheme();
    const questionStore = useQuestionStore();

    const filterDialog = ref(false);

    const availableChapters = computed(() => questionStore.getAllChapters);
    const availableSources = computed(() => questionStore.getAllSources);

    const selectedChapters = ref([]);
    const selectedSources = ref([]);

    // Automatically select all options when they are loaded
    watch(
      [availableChapters, availableSources],
      ([newChapters, newSources]) => {
        if (newChapters && newChapters.length > 0) {
          selectedChapters.value = [...newChapters];
        }
        if (newSources && newSources.length > 0) {
          selectedSources.value = [...newSources];
        }
      },
      { immediate: true }
    );

    function toggleTheme() {
      theme.global.name.value =
        theme.global.name.value === "light" ? "dark" : "light";
    }

    const routeToAbout = () => {
      router.push({ path: "/about" });
    };

    const applyFilters = () => {
      // Implement your filter logic here
      questionStore.selected_chapters = selectedChapters.value;
      questionStore.selected_sources = selectedSources.value;
      questionStore.reSetUpAfterFiltersChange();

      // Close the dialog after applying filters
      filterDialog.value = false;
    };

    const selectAllChapters = () => {
      selectedChapters.value = [...availableChapters.value];
    };

    const deselectAllChapters = () => {
      selectedChapters.value = [];
    };

    const selectAllSources = () => {
      selectedSources.value = [...availableSources.value];
    };

    const deselectAllSources = () => {
      selectedSources.value = [];
    };

    const canApplyFilters = computed(() => {
      return (
        selectedChapters.value.length > 0 && selectedSources.value.length > 0
      );
    });

    return {
      drawer,
      routeToAbout,
      toggleTheme,
      filterDialog,
      applyFilters,
      canApplyFilters,
      availableChapters,
      availableSources,
      selectedChapters,
      selectedSources,
      selectAllChapters,
      deselectAllChapters,
      selectAllSources,
      deselectAllSources,
    };
  },
};
</script>

<style scoped>
h1 {
  color: #42b983;
}

.v-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.v-container {
  flex: 1;
  display: flex;
}
.v-main {
  flex: 1;
}
</style>