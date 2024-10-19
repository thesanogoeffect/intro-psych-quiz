export const useGeneralStore = defineStore("general", {
    state: () => ({
        landingPopup : true,
        instructionsPopup : false,
    }),
    actions: {
        toggleLandingPopup() {
            this.landingPopup = !this.landingPopup;
            // Store the current date in localStorage when the popup is toggled off
            if (!this.landingPopup) {
                const today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format
                localStorage.setItem('landingPopupLastShown', today);
            }
        },
        toggleInstructionsPopup() {
            this.instructionsPopup = !this.instructionsPopup;
        },
        checkLandingPopup() {
            const lastShownDate = localStorage.getItem('landingPopupLastShown');
            const today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format
            if (lastShownDate === today) {
                this.landingPopup = false; // Don't show the popup if it's already been shown today
            } else {
                this.landingPopup = true; // Otherwise, show the popup
            }
        }
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

// You can call the `checkLandingPopup()` action when your app initializes, such as in a component's mounted hook
