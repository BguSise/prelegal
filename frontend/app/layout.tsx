import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NDA Creator",
  description: "Create a Mutual Non-Disclosure Agreement",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
          <header className="border-b bg-white shadow-sm">
            <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
              <h1 className="text-3xl font-bold text-gray-900">NDA Creator</h1>
              <p className="mt-2 text-gray-600">
                Create a Mutual Non-Disclosure Agreement in minutes
              </p>
            </div>
          </header>
          <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
