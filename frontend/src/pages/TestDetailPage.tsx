import { useEffect, useState } from "react";
import { fetchTestDetail, TestDetail } from "../api/tests";

interface Props {
  testCaseId: number;
}

export function TestDetailPage({ testCaseId }: Props) {
  const [detail, setDetail] = useState<TestDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const data = await fetchTestDetail(testCaseId);
        setDetail(data);
        setError(null);
      } catch (err: any) {
        setError(err.message || "Failed to load test detail");
      } finally {
        setLoading(false);
      }
    })();
  }, [testCaseId]);

  if (loading) return <p>Loading test...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!detail) return <p>Test not found.</p>;

  return (
    <div style={{ padding: "1.5rem" }}>
      <button onClick={() => (window.location.hash = "#/flaky")}>← Back</button>
      <h1>{detail.suite_name}::{detail.test_name}</h1>
      <p>
        <strong>Repository:</strong> {detail.repository}
      </p>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: "0.5rem" }}>
        <div><strong>Runs:</strong> {detail.runs}</div>
        <div><strong>Failures:</strong> {detail.failures}</div>
        <div><strong>Passes:</strong> {detail.passes}</div>
        <div><strong>Failure rate:</strong> {detail.failure_rate.toFixed(2)}</div>
        <div><strong>Flakiness:</strong> {detail.flakiness_score.toFixed(2)}</div>
        <div><strong>Last run:</strong> {detail.last_run_at ?? "—"}</div>
      </div>

      <h2 style={{ marginTop: "1rem" }}>Recent runs</h2>
      <table>
        <thead>
          <tr>
            <th>Status</th>
            <th>Commit</th>
            <th>Branch</th>
            <th>Duration (ms)</th>
            <th>Run at</th>
            <th>Error</th>
          </tr>
        </thead>
        <tbody>
          {detail.recent_runs.map((r) => (
            <tr key={r.id}>
              <td>{r.status}</td>
              <td>{r.commit_sha}</td>
              <td>{r.branch}</td>
              <td>{r.duration_ms ?? "—"}</td>
              <td>{r.run_at}</td>
              <td>{r.error_message ?? ""}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
