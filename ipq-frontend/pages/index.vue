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
          <v-btn
            icon="mdi-format-align-right"
            variant="text"
            @click="toggleRightDrawer"
          ></v-btn>
        </v-app-bar>

        <!-- Left Navigation Drawer -->
        <v-navigation-drawer v-model="drawer" location="left" v-if="drawer">
          <LeftSidebar />
        </v-navigation-drawer>

        <!-- Right Navigation Drawer (RightSidebar) -->
        <v-navigation-drawer v-model="rightDrawer" location="right">
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
          <v-card-title class="headline">Question Filter</v-card-title>

          <v-card-text>
            <!-- Chapter Selection -->
            <div class="mb-4">
              <v-select
                multiple
                variant="outlined"
                :items="availableChapters"
                v-model="selectedChapters"
                label="Selected Chapters"
              ></v-select>
              <v-btn text class="mx-2" @click="selectAllChapters"
                >Select All Chapters</v-btn
              >
              <v-btn text class="mx-2" @click="deselectAllChapters"
                >Deselect All Chapters</v-btn
              >

              <v-divider class="my-3"></v-divider>

              <v-btn outlined class="mx-2" @click="selectPreMidtermChapters"
                >Select Pre-Midterm Chapters</v-btn
              >
              <v-btn outlined class="mx-2" @click="selectPostMidtermChapters"
                >Select Post-Midterm Chapters</v-btn
              >
            </div>

            <!-- Source Selection -->
            <div class="mb-4">
              <v-select
                multiple
                variant="outlined"
                :items="availableSources"
                v-model="selectedSources"
                label="Selected Sources"
              ></v-select>
              <v-btn text class="mx-2" @click="selectAllSources"
                >Select All Sources</v-btn
              >
              <v-btn text class="mx-2" @click="deselectAllSources"
                >Deselect All Sources</v-btn
              >
            </div>
          </v-card-text>

          <v-card-actions class="justify-end">
            <v-btn text @click="filterDialog = false">Cancel</v-btn>
            <v-btn
              :disabled="!canApplyFilters"
              color="primary"
              @click="applyFilters"
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
    const display = useDisplay();
    const mdAndUp = computed(() => display.mdAndUp);

    const drawer = ref(mdAndUp.value);
    const rightDrawer = ref(mdAndUp.value);

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

    watch(mdAndUp, (newVal) => {
      drawer.value = newVal;
      rightDrawer.value = newVal;
    });

    function toggleTheme() {
      theme.global.name.value =
        theme.global.name.value === "light" ? "dark" : "light";
    }

    function toggleRightDrawer() {
      rightDrawer.value = !rightDrawer.value;
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

    const selectPreMidtermChapters = () => {
      selectedChapters.value = availableChapters.value.filter(
        (chapter) => chapter >= 1 && chapter <= 6
      );
    };

    const selectPostMidtermChapters = () => {
      selectedChapters.value = availableChapters.value.filter(
        (chapter) => chapter >= 7 && chapter <= 12
      );
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
      rightDrawer,
      toggleRightDrawer,
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
      selectPreMidtermChapters,
      selectPostMidtermChapters,
      selectAllSources,
      deselectAllSources,
    };
  },
};
</script>

<style scoped>
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
.headline {
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  padding-bottom: 10px;
}


.v-card-text {
  padding-bottom: 0;
}

.mb-4 {
  margin-bottom: 16px;
}

.mx-2 {
  margin-left: 8px;
  margin-right: 8px;
}

.my-3 {
  margin-top: 12px;
  margin-bottom: 12px;
}

.justify-end {
  display: flex;
  justify-content: flex-end;
}
</style>
