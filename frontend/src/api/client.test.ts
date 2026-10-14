import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { api, onBackendWaking } from "./client";

const ok = (body: unknown) =>
  new Response(JSON.stringify(body), { status: 200, headers: { "content-type": "application/json" } });

describe("waking a sleeping backend", () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it("retries reads through network errors and 503s, reporting that it is waking", async () => {
    const fetch = vi.fn()
      .mockRejectedValueOnce(new TypeError("Failed to fetch"))
      .mockResolvedValueOnce(new Response("starting", { status: 503 }))
      .mockResolvedValueOnce(ok([]));
    vi.stubGlobal("fetch", fetch);
    const states: boolean[] = [];
    const stop = onBackendWaking((w) => states.push(w));

    const projects = api.listProjects();
    await vi.runAllTimersAsync();

    await expect(projects).resolves.toEqual([]);
    expect(fetch).toHaveBeenCalledTimes(3);
    expect(states).toEqual([false, true, false]);
    stop();
  });

  it("never retries a write", async () => {
    const fetch = vi.fn().mockRejectedValue(new TypeError("Failed to fetch"));
    vi.stubGlobal("fetch", fetch);

    await expect(api.createProject("x")).rejects.toThrow("Failed to fetch");
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("returns a 503 from a write as an error instead of retrying", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("{}", { status: 503 })));
    await expect(api.createProject("x")).rejects.toMatchObject({ status: 503 });
  });
});

describe("wrong API address", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("explains an HTML answer instead of failing to parse it", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response("<!doctype html>", { status: 200, headers: { "content-type": "text/html" } })));
    await expect(api.domains()).rejects.toThrow("returned a web page instead of data");
  });
});

describe("visitor workspace key", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("sends the same random key with every request", async () => {
    const fetch = vi.fn().mockImplementation(async () => ok([]));
    vi.stubGlobal("fetch", fetch);
    await api.listProjects();
    await api.domains();
    const keys = fetch.mock.calls.map(([, init]) => init.headers["X-Autevra-Workspace"]);
    expect(keys[0]).toMatch(/^[0-9a-f]{32}$/);
    expect(keys[1]).toBe(keys[0]);
  });
});
