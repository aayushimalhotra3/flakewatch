import { request } from "./client";

export interface FlakyTestSummary {
  test_case_id: number;
  repository: string;
  suite_name: string;
  test_name: string;
  runs: number;
  failures: number;
  passes: number;
  failure_rate: number;
  flakiness_score: number;
  last_run_at: string | null;
}

export interface TestRunSummary {
  id: number;
  status: string;
  commit_sha: string;
  branch: string;
  duration_ms: number | null;
  run_at: string;
  error_message: string | null;
}

export interface TestDetail {
  test_case_id: number;
  repository: string;
  suite_name: string;
  test_name: string;
  runs: number;
  failures: number;
  passes: number;
  failure_rate: number;
  flakiness_score: number;
  last_run_at: string | null;
  recent_runs: TestRunSummary[];
}

export async function fetchFlakyTests(): Promise<FlakyTestSummary[]> {
  return request("/tests/flaky?limit=50&min_runs=3");
}

export async function fetchTestDetail(id: number): Promise<TestDetail> {
  return request(`/tests/${id}`);
}
