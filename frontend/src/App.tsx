import { useEffect, useState } from "react";
import { FlakyTestsPage } from "./pages/FlakyTestsPage";
import { TestDetailPage } from "./pages/TestDetailPage";

function useRoute() {
  const [hash, setHash] = useState(window.location.hash || "#/flaky");

  useEffect(() => {
    const onHashChange = () => setHash(window.location.hash || "#/flaky");
    window.addEventListener("hashchange", onHashChange);
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  if (hash.startsWith("#/tests/")) {
    const idStr = hash.replace("#/tests/", "");
    const id = Number(idStr);
    return { page: "detail" as const, id };
  }
  return { page: "flaky" as const };
}

function App() {
  const route = useRoute();

  if (route.page === "detail" && route.id > 0) {
    return <TestDetailPage testCaseId={route.id} />;
  }

  return <FlakyTestsPage />;
}

export default App;
