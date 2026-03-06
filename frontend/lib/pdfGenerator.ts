"use client";

import jsPDF from "jspdf";

export function generatePDF(
  content: string,
  filename: string = "nda.pdf"
): void {
  try {
    // Create a new PDF document
    const pdf = new jsPDF({
      orientation: "portrait",
      unit: "mm",
      format: "a4",
    });

    // Set font properties
    pdf.setFont("helvetica", "normal");
    pdf.setFontSize(11);

    // Split content into lines that fit the page width
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const margin = 15;
    const maxWidth = pageWidth - 2 * margin;

    // Split text into lines
    const lines = pdf.splitTextToSize(content, maxWidth);

    // Add content to PDF
    let yPosition = margin;
    const lineHeight = 7;

    lines.forEach((line: string) => {
      if (yPosition + lineHeight > pageHeight - margin) {
        // Add new page if we've reached the bottom
        pdf.addPage();
        yPosition = margin;
      }
      pdf.text(line, margin, yPosition);
      yPosition += lineHeight;
    });

    // Save the PDF
    pdf.save(filename);
  } catch (error) {
    console.error("Error generating PDF:", error);
    throw error;
  }
}
