"use client";

import { useState, useEffect } from "react";
import NDAForm from "@/components/NDAForm";
import DocumentPreview from "@/components/DocumentPreview";
import { loadTemplate, Template } from "@/lib/templateLoader";
import { renderTemplate, formatDate, hasUnreplacedPlaceholders } from "@/lib/documentRenderer";
import { generatePDF } from "@/lib/pdfGenerator";

export default function Home() {
  const [template, setTemplate] = useState<Template | null>(null);
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [renderedContent, setRenderedContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load template on mount
  useEffect(() => {
    const loadNDATemplate = async () => {
      try {
        setLoading(true);
        const loadedTemplate = await loadTemplate("nda-mutual");
        setTemplate(loadedTemplate);

        // Initialize form data with default values
        const initialData: Record<string, any> = {};
        Object.entries(loadedTemplate.fields).forEach(([fieldName, field]) => {
          if (field.default !== undefined) {
            initialData[fieldName] = field.default;
          }
        });
        setFormData(initialData);
        setError(null);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load template"
        );
      } finally {
        setLoading(false);
      }
    };

    loadNDATemplate();
  }, []);

  // Update rendered content when template or form data changes
  useEffect(() => {
    if (template) {
      const dataToRender = { ...formData };
      // Format date fields for display
      if (dataToRender.effectiveDate) {
        dataToRender.effectiveDate = formatDate(dataToRender.effectiveDate);
      }
      const rendered = renderTemplate(template.content, dataToRender);
      setRenderedContent(rendered);
    }
  }, [template, formData]);

  const handleFormChange = (fieldName: string, value: any) => {
    setFormData((prev) => ({
      ...prev,
      [fieldName]: value,
    }));
  };

  const handleDownloadPDF = () => {
    if (!template) return;

    try {
      const dataForPDF = { ...formData };
      // Format date for PDF
      if (dataForPDF.effectiveDate) {
        dataForPDF.effectiveDate = formatDate(dataForPDF.effectiveDate);
      }
      const content = renderTemplate(template.content, dataForPDF);

      // Validate that all required placeholders have been replaced
      if (hasUnreplacedPlaceholders(content)) {
        setError(
          "Please fill in all required fields before downloading the document."
        );
        return;
      }

      const partyA = formData.partyA || "Party A";
      const filename = `${partyA.replace(/\s+/g, "_")}_NDA_Mutual.pdf`;
      generatePDF(content, filename);
      setError(null);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to generate PDF"
      );
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full border-4 border-blue-200 border-t-blue-600 h-8 w-8"></div>
          <p className="mt-4 text-gray-600">Loading template...</p>
        </div>
      </div>
    );
  }

  if (error || !template) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-4">
        <h3 className="font-semibold text-red-900">Error</h3>
        <p className="mt-2 text-sm text-red-700">
          {error || "Failed to load template"}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="grid gap-8 lg:grid-cols-2">
        {/* Form Section */}
        <div>
          <NDAForm
            template={template}
            formData={formData}
            onChange={handleFormChange}
          />
        </div>

        {/* Preview Section */}
        <div>
          <DocumentPreview content={renderedContent} />
        </div>
      </div>

      {/* Download Button */}
      <div className="flex flex-col items-center gap-4">
        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 w-full max-w-md text-center">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}
        <button
          onClick={handleDownloadPDF}
          className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
        >
          Download as PDF
        </button>
      </div>
    </div>
  );
}
