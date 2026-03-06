"use client";

interface DocumentPreviewProps {
  content: string;
}

export default function DocumentPreview({ content }: DocumentPreviewProps) {
  // Format the content for display with proper line breaks and spacing
  const formattedContent = content.split("\n").map((line, index) => {
    // Add extra spacing for section headers (numbered sections)
    if (/^\d+\./.test(line)) {
      return (
        <div key={index} className="mt-4 mb-2">
          <p className="font-semibold text-gray-900">{line}</p>
        </div>
      );
    }

    // Add spacing for "IN WITNESS WHEREOF" section
    if (line.includes("IN WITNESS WHEREOF")) {
      return (
        <div key={index} className="mt-6 mb-2">
          <p className="font-semibold text-gray-900">{line}</p>
        </div>
      );
    }

    // Highlight party signatures
    if (/^(PARTY|DISCLOSING PARTY|RECEIVING PARTY):/.test(line)) {
      return (
        <div key={index} className="mt-4 mb-2">
          <p className="font-semibold text-gray-900">{line}</p>
        </div>
      );
    }

    // Skip empty lines but preserve spacing
    if (line.trim() === "") {
      return <div key={index} className="h-2" />;
    }

    // Regular paragraphs
    return (
      <p key={index} className="text-gray-700 leading-relaxed">
        {line}
      </p>
    );
  });

  return (
    <div className="bg-white p-8 shadow rounded-lg">
      <h2 className="mb-6 text-xl font-semibold text-gray-900">
        Document Preview
      </h2>
      <div className="prose prose-sm max-w-none space-y-2 text-sm text-gray-800">
        {formattedContent}
      </div>
    </div>
  );
}
