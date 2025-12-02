import { useEffect, useState } from "react";
import { fetchFlakyTests, FlakyTestSummary } from "../api/tests";

export function FlakyTestsPage() {
  const [tests, setTests] = useState<FlakyTestSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const data = await fetchFlakyTests();
        setTests(data);
        setError(null);
      } catch (err: any) {
        setError(err.message || "Failed to load flaky tests");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <p>Loading flaky tests...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!tests.length) return <p>No flaky tests found yet.</p>;

  return (
    <div style={{ padding: "1.5rem" }}>
      <h1>FlakeWatch</h1>
      <h2>Top flaky tests</h2>
      <table>
        <thead>
          <tr>
            <th>Test</th>
            <th>Repository</th>
            <th>Runs</th>
            <th>Failures</th>
            <th>Flakiness</th>
            <th>Last run</th>
          </tr>
        </thead>
        <tbody>
          {tests.map((t) => (
            <tr
              key={t.test_case_id}
              style={{ cursor: "pointer" }}
              onClick={() => {
                window.location.hash = `#/tests/${t.test_case_id}`;
              }}
            >
              <td>{t.suite_name}::{t.test_name}</td>
              <td>{t.repository}</td>
              <td>{t.runs}</td>
              <td>{t.failures}</td>
              <td>{t.flakiness_score.toFixed(2)}</td>
              <td>{t.last_run_at ?? "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
