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

import { apiClient } from "./api";

export async function loadTemplate(templateId: string): Promise<Template> {
  try {
    return await apiClient.get<Template>(`/templates/${templateId}`);
  } catch (error) {
    console.error("Error loading template:", error);
    throw error;
  }
}

export async function loadTemplateIndex(): Promise<any[]> {
  try {
    const templates = await apiClient.get<any[]>("/templates");
    return templates;
  } catch (error) {
    console.error("Error loading template index:", error);
    throw error;
  }
}
