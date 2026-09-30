export function getUserIdFromToken(token: string): string | null {
  try { 
    const payload = token.split('.')[1];
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
    const json = atob(base64); // it will convert the base64 encoding into its actuall json
    const decoded = JSON.parse(json);
    return decoded.user_id ?? null;
  } catch {
    return null;
  }
}