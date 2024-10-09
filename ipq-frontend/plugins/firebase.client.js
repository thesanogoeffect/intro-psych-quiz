import { getFirestore, collection } from "firebase/firestore";

export default defineNuxtPlugin((nuxtApp) => {
  const db = getFirestore(nuxtApp.$firebaseApp);
  const questionsRef = collection(db, "questions");

  return {
    provide: {
      db,
      questionsRef,
    },
  };
});