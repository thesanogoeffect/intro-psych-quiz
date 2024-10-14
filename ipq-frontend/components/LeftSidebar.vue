<template>
    <div v-if="isStoreInitialized">
        {{ userStore.getAnsweredQuestions }}
        {{ userStore.getTotalCorrectAnswers }}
        <div v-if="userStore.getAnsweredQuestions>0">
        {{ userStore.getAnsweredCorrectlyPercentage }}
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            isStoreInitialized: false,
            userStore: null
        };
    },
    created() {
        try {
            this.userStore = useQuestionStore();
            this.isStoreInitialized = true;
        } catch (error) {
            console.error('Pinia store is not initialized:', error);
        }
    }
};
</script>