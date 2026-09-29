// Heliotrope auth — session-based, family accounts, long-lived "cached login".
//
// Design (see docs/architecture.md):
// - Opaque 256-bit session tokens stored server-side in D1; the cookie is
//   httpOnly + Secure + SameSite=Lax so JS can never read it.
// - Passwords hashed with PBKDF2-SHA256 (210k iterations, per-password salt)
//   via the WebCrypto API that Workers provide. Never plaintext, never logs.
// - Sessions live 90 days and slide on use ("cached login" — she hates
//   re-logging in). Rotation: a fresh token is issued periodically and on
//   privilege changes; old tokens are revoked.
// - Every personal-data table carries user_id; auth middleware attaches the
//   user and their permitted scope (own data + granted shares).

const PBKDF2_ITERATIONS = 210_000;
const SESSION_TTL_MS = 90 * 24 * 60 * 60 * 1000; // 90 days

const b64 = (buf) =>
  btoa(String.fromCharCode(...new Uint8Array(buf)));
const unb64 = (s) =>
  Uint8Array.from(atob(s), (c) => c.charCodeAt(0));

export function randomToken() {
  return b64(crypto.getRandomValues(new Uint8Array(32))); // 256-bit
}

export async function hashPassword(password) {
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(password),
    "PBKDF2",
    false,
    ["deriveBits"],
  );
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", hash: "SHA-256", salt, iterations: PBKDF2_ITERATIONS },
    key,
    256,
  );
  return `pbkdf2-sha256$${PBKDF2_ITERATIONS}$${b64(salt)}$${b64(bits)}`;
}

export async function verifyPassword(password, stored) {
  try {
    const [algo, iter, saltB64, hashB64] = stored.split("$");
    if (algo !== "pbkdf2-sha256") return false;
    const salt = unb64(saltB64);
    const key = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode(password),
      "PBKDF2",
      false,
      ["deriveBits"],
    );
    const bits = await crypto.subtle.deriveBits(
      { name: "PBKDF2", hash: "SHA-256", salt, iterations: Number(iter) },
      key,
      256,
    );
    const a = unb64(hashB64);
    const b = new Uint8Array(bits);
    if (a.length !== b.length) return false;
    let diff = 0;
    for (let i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
    return diff === 0;
  } catch {
    return false;
  }
}

export function sessionCookie(token, env) {
  const secure = env.APP_ENV === "local" ? "" : "; Secure";
  const maxAge = Math.floor(SESSION_TTL_MS / 1000);
  return `${env.COOKIE_NAME}=${encodeURIComponent(token)}; HttpOnly${secure}; SameSite=Lax; Path=/; Max-Age=${maxAge}`;
}

export function clearSessionCookie(env) {
  return `${env.COOKIE_NAME}=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0`;
}

function getCookieToken(request, env) {
  const raw = request.headers.get("cookie") || "";
  const m = raw.match(new RegExp(`(?:^|;\\s*)${env.COOKIE_NAME}=([^;]+)`));
  return m ? decodeURIComponent(m[1]) : null;
}

async function sha256Hex(s) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(d)].map((x) => x.toString(16).padStart(2, "0")).join("");
}

/** Create a session row and return the raw token (sent to the client once). */
export async function createSession(db, userId) {
  const token = randomToken();
  const tokenHash = await sha256Hex(token);
  const now = Date.now();
  await db
    .prepare(
      `INSERT INTO sessions (token_hash, user_id, created_at, last_seen_at, expires_at)
       VALUES (?, ?, ?, ?, ?)`,
    )
    .bind(tokenHash, userId, now, now, now + SESSION_TTL_MS)
    .run();
  return token;
}

export async function revokeSession(db, token) {
  const tokenHash = await sha256Hex(token);
  await db.prepare("DELETE FROM sessions WHERE token_hash = ?").bind(tokenHash).run();
}

/**
 * Auth middleware: resolves the session cookie to { user, scope } and puts it
 * on ctx. Scope = own user_id plus any owner_ids shared with them via grants.
 * Returns a Response to short-circuit (401/403) or null to continue.
 */
export async function authMiddleware(request, env, ctx) {
  const token = getCookieToken(request, env);
  if (!token) return unauthorized();

  const tokenHash = await sha256Hex(token);
  const row = await env.DB.prepare(
    `SELECT s.user_id, s.expires_at, u.id, u.display_name, u.role
     FROM sessions s JOIN users u ON u.id = s.user_id
     WHERE s.token_hash = ?`,
  )
    .bind(tokenHash)
    .first();
  if (!row || row.expires_at < Date.now()) {
    if (row) await revokeSession(env.DB, token);
    return unauthorized();
  }

  // Sliding window: extend the session on use ("cached login").
  await env.DB.prepare(
    "UPDATE sessions SET last_seen_at = ?, expires_at = ? WHERE token_hash = ?",
  )
    .bind(Date.now(), Date.now() + SESSION_TTL_MS, tokenHash)
    .run();

  // Family sharing: owner_ids this user may read, granted by the owner.
  const grants = await env.DB.prepare(
    `SELECT owner_id FROM shares WHERE viewer_id = ? AND revoked_at IS NULL`,
  )
    .bind(row.user_id)
    .all();

  ctx.user = { id: row.id, displayName: row.display_name, role: row.role };
  ctx.scope = {
    ownId: row.user_id,
    readableUserIds: [
      row.user_id,
      ...(grants.results || []).map((g) => g.owner_id),
    ],
  };
  return null;
}

function unauthorized() {
  return new Response(JSON.stringify({ error: "unauthorized" }), {
    status: 401,
    headers: { "content-type": "application/json" },
  });
}

/** Scope guard for queries: WHERE user_id IN (...readableUserIds). */
export function scopePlaceholders(ctx) {
  return ctx.scope.readableUserIds.map(() => "?").join(", ");
}
