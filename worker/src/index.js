// Heliotrope API — Cloudflare Worker + D1 (+ R2 for photos).
//
// Phase 1 skeleton: minimal router, D1/R2 bindings, auth middleware.
// Endpoint handlers beyond auth + health + digest are 501 stubs for later teams.

import {
  authMiddleware,
  clearSessionCookie,
  createSession,
  revokeSession,
  sessionCookie,
  verifyPassword,
} from "./auth.js";

const json = (data, status = 200, headers = {}) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json", ...headers },
  });

function getToken(request, env) {
  const raw = request.headers.get("cookie") || "";
  const m = raw.match(new RegExp(`(?:^|;\\s*)${env.COOKIE_NAME}=([^;]+)`));
  return m ? decodeURIComponent(m[1]) : null;
}

// export default { ... } continues below

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const { pathname } = url;

    // Public: health + login. Everything else under /api requires a session.
    if (pathname === "/api/health") {
      return json({ ok: true, app: "heliotrope", phase: 1 });
    }
    if (pathname === "/api/auth/login" && request.method === "POST") {
      return handleLogin(request, env);
    }
    if (pathname === "/api/auth/logout" && request.method === "POST") {
      return handleLogout(request, env);
    }

    // Service-to-service ingest (cron job files chat digests here).
    if (pathname === "/api/digest" && request.method === "POST") {
      return handleDigest(request, env);
    }

    // All remaining /api/* routes need an authenticated session.
    if (pathname.startsWith("/api/")) {
      const authed = await authMiddleware(request, env, ctx);
      if (authed) return authed;
      return routeApi(request, env, ctx, pathname);
    }

    // Static frontend (apps/web) served by the Pages/Workers static asset
    // setup in a later phase. Phase 1: friendly pointer.
    return new Response("Heliotrope API — frontend lands in a later phase.", {
      status: 200,
      headers: { "content-type": "text/plain" },
    });
  },
};

async function handleLogin(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "invalid json" }, 400);
  }
  const { username, password } = body || {};
  if (!username || !password) return json({ error: "username and password required" }, 400);

  // TODO(phase 2): rate-limit login attempts per IP/username (see docs/architecture.md).
  const user = await env.DB.prepare(
    "SELECT id, username, password_hash, display_name, role FROM users WHERE username = ?",
  )
    .bind(String(username).toLowerCase())
    .first();
  if (!user || !(await verifyPassword(password, user.password_hash))) {
    // Same response either way: don't reveal which half was wrong.
    return json({ error: "invalid credentials" }, 401);
  }

  const token = await createSession(env.DB, user.id);
  return json(
    { ok: true, user: { id: user.id, displayName: user.display_name, role: user.role } },
    200,
    { "set-cookie": sessionCookie(token, env) },
  );
}

async function handleLogout(request, env) {
  const token = getToken(request, env);
  if (token) await revokeSession(env.DB, token);
  return json({ ok: true }, 200, { "set-cookie": clearSessionCookie(env) });
}

/**
 * POST /api/digest — ingest a daily chat-summary payload from the scheduled job.
 * Auth: shared service secret in the Authorization header (Bearer), stored as
 * a Worker secret (DIGEST_INGEST_SECRET), never in git. NOT user-authenticated.
 */
async function handleDigest(request, env) {
  const auth = request.headers.get("authorization") || "";
  const expected = env.DIGEST_INGEST_SECRET;
  if (!expected || auth !== `Bearer ${expected}`) {
    return json({ error: "unauthorized" }, 401);
  }
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "invalid json" }, 400);
  }
  const { title, date, summary_markdown, health_facts } = body || {};
  if (!title || !date || !summary_markdown) {
    return json({ error: "title, date, and summary_markdown are required" }, 400);
  }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
    return json({ error: "date must be YYYY-MM-DD" }, 400);
  }
  const result = await env.DB.prepare(
    `INSERT INTO digests (title, digest_date, summary_markdown, health_facts_json, created_at)
     VALUES (?, ?, ?, ?, ?)`,
  )
    .bind(
      title,
      date,
      summary_markdown,
      JSON.stringify(health_facts || []),
      new Date().toISOString(),
    )
    .run();
  return json({ ok: true, id: Number(result.meta.last_row_id) }, 201);
}

/** Phase 1: every domain route returns 501 with its planned shape (see docs/api.md). */
async function routeApi(request, env, ctx, pathname) {
  const method = request.method;
  const stubs = [
    ["/api/today", "GET"],
    ["/api/body/systems", "GET"],
    ["/api/meds", "GET"],
    ["/api/meds", "POST"],
    ["/api/labs", "GET"],
    ["/api/care-team", "GET"],
    ["/api/todos", "GET"],
    ["/api/todos", "POST"],
    ["/api/nourish", "GET"],
    ["/api/nourish", "POST"],
    ["/api/cycle", "GET"],
    ["/api/stress", "GET"],
    ["/api/skin", "GET"],
    ["/api/weight", "GET"],
    ["/api/mind/entries", "GET"],
    ["/api/orders", "GET"],
    ["/api/reports/visit-summary", "GET"],
    ["/api/photos/upload", "POST"],
  ];
  const hit = stubs.find(([p, m]) => p === pathname && m === method);
  if (hit) {
    return json(
      { error: "not implemented", phase: 2, route: `${method} ${pathname}` },
      501,
    );
  }
  return json({ error: "not found" }, 404);
}
