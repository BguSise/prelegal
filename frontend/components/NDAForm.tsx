"use client";

import { Template } from "@/lib/templateLoader";
import { ChangeEvent } from "react";

interface NDAFormProps {
  template: Template;
  formData: Record<string, any>;
  onChange: (fieldName: string, value: any) => void;
}

export default function NDAForm({
  template,
  formData,
  onChange,
}: NDAFormProps) {
  const handleInputChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    onChange(name, value);
  };

  return (
    <form className="space-y-6 bg-white p-6 shadow rounded-lg">
      <h2 className="text-xl font-semibold text-gray-900">
        {template.name} Form
      </h2>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {Object.entries(template.fields).map(([fieldName, field]) => {
          const value = formData[fieldName] ?? "";

          return (
            <div key={fieldName} className={field.type === "textarea" ? "md:col-span-2" : ""}>
              <label
                htmlFor={fieldName}
                className="block text-sm font-medium text-gray-700"
              >
                {field.label}
                {field.required && (
                  <span className="ml-1 text-red-500">*</span>
                )}
              </label>

              {field.type === "textarea" ? (
                <textarea
                  id={fieldName}
                  name={fieldName}
                  value={value}
                  onChange={handleInputChange}
                  placeholder={field.placeholder}
                  required={field.required}
                  rows={4}
                  className="mt-2 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              ) : (
                <input
                  id={fieldName}
                  type={field.type}
                  name={fieldName}
                  value={value}
                  onChange={handleInputChange}
                  placeholder={field.placeholder}
                  required={field.required}
                  className="mt-2 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              )}

              {field.type === "number" && field.default && !value && (
                <p className="mt-1 text-xs text-gray-500">
                  Default: {field.default}
                </p>
              )}
            </div>
          );
        })}
      </div>
    </form>
  );
}
