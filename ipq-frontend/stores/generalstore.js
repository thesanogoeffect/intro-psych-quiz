export const useGeneralStore = defineStore("general", {
    state: () => ({
        landingPopup : false,
    }),
    actions: {
        toggleLandingPopup() {
            this.landingPopup = !this.landingPopup;
        },
    },
    getters: {
        getLandingPopup() {
            return this.landingPopup;
        },
    },
});