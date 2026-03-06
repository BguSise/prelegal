export function renderTemplate(
  template: string,
  data: Record<string, any>
): string {
  let rendered = template;

  // Replace all {{fieldName}} placeholders with actual values
  Object.entries(data).forEach(([key, value]) => {
    // Escape regex special characters in key and create placeholder pattern
    const escapedKey = key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const placeholder = new RegExp(`\\{\\{${escapedKey}\\}\\}`, "g");
    rendered = rendered.replace(placeholder, String(value || ""));
  });

  return rendered;
}

export function hasUnreplacedPlaceholders(content: string): boolean {
  // Check if there are any unreplaced {{...}} placeholders
  return /\{\{[^}]+\}\}/.test(content);
}

export function formatDate(dateString: string): string {
  if (!dateString) return "";
  // Parse ISO 8601 date in local time to avoid UTC off-by-one error
  const [year, month, day] = dateString.split("-").map(Number);
  const date = new Date(year, month - 1, day);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}
