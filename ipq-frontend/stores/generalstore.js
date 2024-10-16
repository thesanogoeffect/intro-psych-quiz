export const useGeneralStore = defineStore("general", {
    state: () => ({
        landingPopup : true,
        instructionsPopup : false,
    }),
    actions: {
        toggleLandingPopup() {
            this.landingPopup = !this.landingPopup;
        },
        toggleInstructionsPopup() {
            this.instructionsPopup = !this.instructionsPopup;
        },
    },
    getters: {
        getLandingPopup() {
            return this.landingPopup;
        },
        getInstructionsPopup() {
            return this.instructionsPopup;
        },
    },
});