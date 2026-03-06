export interface TemplateField {
  label: string;
  type: "text" | "email" | "date" | "textarea" | "number";
  required: boolean;
  placeholder?: string;
  default?: string | number;
}

export interface Template {
  id: string;
  name: string;
  category: string;
  version: string;
  createdDate: string;
  fields: Record<string, TemplateField>;
  content: string;
}

export async function loadTemplate(templateId: string): Promise<Template> {
  try {
    const response = await fetch(
      `/templates/${templateId}.json`
    );
    if (!response.ok) {
      throw new Error(`Failed to load template: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error loading template:", error);
    throw error;
  }
}

export async function loadTemplateIndex(): Promise<any[]> {
  try {
    const response = await fetch("/templates/index.json");
    if (!response.ok) {
      throw new Error(`Failed to load template index: ${response.statusText}`);
    }
    const data = await response.json();
    return data.templates;
  } catch (error) {
    console.error("Error loading template index:", error);
    throw error;
  }
}
