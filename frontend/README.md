# NDA Creator Frontend

A Next.js web application for creating Mutual Non-Disclosure Agreements (NDAs).

## Features

- **Interactive Form**: User-friendly form to collect NDA details
- **Real-time Preview**: See the document as you fill out the form
- **PDF Export**: Download the completed NDA as a PDF file
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **PDF Generation**: jsPDF
- **Runtime**: React 19

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Project Structure

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Main page component
└── globals.css         # Global styles

components/
├── NDAForm.tsx         # Form component
└── DocumentPreview.tsx # Document preview component

lib/
├── templateLoader.ts   # Template loading utilities
├── documentRenderer.ts # Template rendering utilities
└── pdfGenerator.ts     # PDF generation utilities

public/
└── templates/          # Legal template JSON files
```

## How It Works

1. **Load Template**: The app loads the Mutual NDA template from the templates directory
2. **Collect Input**: User fills in the form fields
3. **Real-time Rendering**: The document preview updates as the user types
4. **Export PDF**: User can download the completed document as PDF

## Template Structure

Templates are JSON files with the following structure:
- `fields`: Form field definitions with types and validation
- `content`: Template content with `{{fieldName}}` placeholders
- Placeholders are replaced with user-provided values

## Development

The app uses:
- **Type Safety**: Full TypeScript support
- **Component-based Architecture**: Reusable React components
- **Client-side Rendering**: All processing happens in the browser
- **Responsive Design**: Mobile-first approach with Tailwind CSS

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
