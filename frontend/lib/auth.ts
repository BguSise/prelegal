/**
 * Authentication utilities for token management and auth state.
 */

const TOKEN_KEY = 'prelegal_token';

export function storeToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_KEY, token);
  }
}

export function getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_KEY);
  }
  return null;
}

export function removeToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY);
  }
}

export function isAuthenticated(): boolean {
  const token = getToken();
  if (!token) return false;

  // Basic check: decode the token and verify it hasn't expired
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return false;

    // Decode payload (JWT format: header.payload.signature)
    const payload = JSON.parse(atob(parts[1]));
    const now = Math.floor(Date.now() / 1000);

    // Check if token has expired
    if (payload.exp && payload.exp <= now) {
      removeToken();
      return false;
    }

    return true;
  } catch {
    return false;
  }
}

export function clearAuth(): void {
  removeToken();
}
