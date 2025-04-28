# Data Templates

This directory contains template data files that should be copied to the `data/` directory
when setting up a new installation.

The `data/` directory itself is gitignored as it typically contains user-generated content
and configuration, but these templates provide the initial structure and example files.

## How to use

When setting up a new instance of Medocker:

1. Copy all files from this directory to the `data/` directory
2. Modify as needed for your specific installation

```bash
# Example command to copy all templates
cp -r data-templates/* data/
```

## Template Files

- `service_catalog.json` - Catalog of available services for the cart page
- `test.json` - Test file used for checking volume mounting 