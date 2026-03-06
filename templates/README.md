# Legal Document Templates Dataset

This directory contains a curated dataset of legal document templates for the prelegal platform. Each template is designed to be customizable and modifiable for different user needs.

## Structure

### `index.json`
The main index file listing all available templates with metadata including:
- Template ID
- Template name
- Category (e.g., contracts, employment, policies, intellectual-property)
- Description
- List of customizable fields
- Last updated date

### Individual Template Files
Each template is stored as a separate JSON file with the following structure:

```json
{
  "id": "template-id",
  "name": "Template Name",
  "category": "category-name",
  "version": "1.0",
  "createdDate": "YYYY-MM-DD",
  "fields": {
    "fieldName": {
      "label": "Display Label",
      "type": "text|email|date|textarea|number",
      "required": true|false,
      "placeholder": "Example text",
      "default": "Default value (optional)"
    }
  },
  "content": "Template content with {{placeholder}} variables"
}
```

## Available Templates

### Intellectual Property
- **nda-unilateral.json** - One-way Non-Disclosure Agreement
- **nda-mutual.json** - Mutual Non-Disclosure Agreement (coming soon)
- **licensing-agreement.json** - Software Licensing Agreement (coming soon)

### Contracts
- **service-agreement.json** - Standard Service Agreement
- **contractor-agreement.json** - Independent Contractor Agreement

### Employment
- **employment-contract.json** - Full-time Employment Contract

### Policies
- **privacy-policy.json** - Privacy Policy for web/SaaS platforms
- **tos-saas.json** - Terms of Service for SaaS (coming soon)

### Real Estate
- **rental-agreement.json** - Rental/Lease Agreement (coming soon)

### Transactions
- **purchase-agreement.json** - Purchase Agreement (coming soon)

## Field Types

- **text**: Single-line text input
- **email**: Email address input with validation
- **date**: Date picker input
- **textarea**: Multi-line text input
- **number**: Numeric input

## Usage

### For Template Developers
1. Each template can be modified by updating the content field
2. Fields can be added or removed by modifying the `fields` object
3. The `content` field uses `{{fieldName}}` syntax for variable substitution
4. Update the `version` and `createdDate` when making changes

### For System Integration
1. Parse the `index.json` to discover available templates
2. Load individual template files as needed
3. Replace `{{fieldName}}` placeholders with user-provided values
4. Generate the final document

## Placeholder Syntax

Templates use `{{fieldName}}` syntax for variable substitution. The field name must match exactly with a field defined in the `fields` object.

Example:
```
Agreement between {{companyName}} and {{clientName}}
```

## Future Enhancements

- Support for conditional fields (showing/hiding based on other field values)
- Template versioning and migration support
- Multi-language support
- Rich text formatting support
- Signature and date fields with automatic handling
- Template categories and tags for better discovery
- Default field values and auto-population
- Template variants for different jurisdictions

## Contributing

To add a new template:

1. Create a new JSON file following the structure above
2. Add an entry to `index.json`
3. Test the template with sample data
4. Update this README with the new template information

---

Last updated: 2025-03-06
