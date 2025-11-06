---
name: gotenberg
description: Gotenberg document conversion API. Use for converting HTML, Markdown, Office documents to PDF, document merging, and automated document generation.
---

# Gotenberg Skill

Comprehensive assistance with Gotenberg - a Docker-powered stateless API for converting HTML, Markdown, and Office documents to PDF. Gotenberg uses Chromium and LibreOffice engines to provide high-quality document conversion with extensive customization options.

## When to Use This Skill

This skill should be triggered when you need to:

**Document Conversion Tasks:**
- Convert web pages or HTML files to PDF
- Transform Markdown documents to PDF with custom styling
- Convert Office documents (Word, Excel, PowerPoint) to PDF
- Generate PDFs programmatically from any web content

**PDF Manipulation:**
- Merge multiple PDF files into one document
- Split PDF files by page ranges or intervals
- Convert PDFs to PDF/A format for archival compliance
- Add or modify PDF metadata
- Flatten PDF forms and annotations

**Advanced PDF Generation:**
- Create PDFs with custom headers and footers
- Generate PDFs with specific page properties (size, margins, orientation)
- Handle JavaScript-heavy websites requiring render delays
- Capture screenshots of web pages in various formats (PNG, JPEG, WebP)

**API Integration & Automation:**
- Set up asynchronous PDF generation with webhooks
- Configure Gotenberg Docker containers with custom settings
- Implement document generation in web applications
- Troubleshoot Gotenberg conversion issues

## Key Concepts

### Architecture
- **Stateless API**: Gotenberg runs as a Docker container exposing HTTP endpoints
- **Multi-Engine**: Uses Chromium for HTML/web conversion, LibreOffice for Office documents
- **Queue-Based**: Single engine instances process requests sequentially (scale horizontally for concurrency)
- **Form Data**: All routes accept `multipart/form-data` requests

### Core Modules
- **Chromium Module**: Converts HTML, URLs, and Markdown to PDF using headless Chrome
- **LibreOffice Module**: Converts Office documents (.docx, .xlsx, .pptx, etc.) to PDF
- **PDF Engines Module**: Manipulates PDFs (merge, split, convert to PDF/A)
- **Webhook Module**: Enables asynchronous file uploads to external endpoints
- **API Module**: HTTP/1 and HTTP/2 server with configurable timeouts and limits

### Important Concepts
- **Trace Header**: `Gotenberg-Trace` header tracks requests through logs and webhooks
- **Output Filename**: `Gotenberg-Output-Filename` header controls the generated PDF name
- **Page Properties**: Control paper size, margins, orientation, and page ranges
- **Wait Mechanisms**: `waitDelay` and `waitForExpression` ensure JavaScript completes before rendering
- **Network Idle Events**: Control when Chromium considers a page fully loaded

## Quick Reference

### 1. Basic URL to PDF Conversion

**Description**: Convert any web page to PDF with a single curl command

```bash
curl --request POST http://localhost:3000/forms/chromium/convert/url \
  --form url=https://my.url \
  -o my.pdf
```

### 2. HTML File to PDF with Assets

**Description**: Convert local HTML with images and stylesheets (assets must be at root level)

```bash
curl --request POST http://localhost:3000/forms/chromium/convert/html \
  --form files=@index.html \
  --form files=@style.css \
  --form files=@logo.png \
  -o output.pdf
```

**HTML Requirements**:
```html
<!-- Paths must be at root level -->
<img src="logo.png" />  <!-- ✓ Works -->
<link rel="stylesheet" href="style.css" />  <!-- ✓ Works -->

<!-- Relative paths won't work -->
<img src="./images/logo.png" />  <!-- ✗ Fails -->
```

### 3. Markdown to PDF Conversion

**Description**: Convert Markdown files with custom HTML template using `toHTML` function

```bash
curl --request POST http://localhost:3000/forms/chromium/convert/markdown \
  --form files=@index.html \
  --form files=@content.md \
  -o output.pdf
```

**Template Example** (index.html):
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial; margin: 40px; }
    code { background: #f4f4f4; padding: 2px 5px; }
  </style>
</head>
<body>
  {{ toHTML "content.md" }}
</body>
</html>
```

### 4. Docker Configuration with Custom Settings

**Description**: Run Gotenberg with custom module properties

**Docker CLI**:
```bash
docker run --rm -p "3000:3000" gotenberg/gotenberg:8 \
  gotenberg \
  --my-module-property=foo
```

**Docker Compose**:
```yaml
services:
  gotenberg:
    image: gotenberg/gotenberg:8
    command:
      - "gotenberg"
      - "--my-module-property=foo"
    ports:
      - "3000:3000"
```

### 5. Custom Page Properties

**Description**: Set paper size, margins, orientation, and page ranges

```bash
curl --request POST http://localhost:3000/forms/chromium/convert/url \
  --form url=https://example.com \
  --form paperWidth=8.5 \
  --form paperHeight=11 \
  --form marginTop=1 \
  --form marginBottom=1 \
  --form marginLeft=0.5 \
  --form marginRight=0.5 \
  --form landscape=false \
  --form nativePageRanges="1-5,8,11-13" \
  -o output.pdf
```

**Common Paper Sizes** (width x height in inches):
- Letter: 8.5 x 11
- Legal: 8.5 x 14
- A4: 8.27 x 11.7
- Tabloid: 11 x 17

### 6. Headers and Footers

**Description**: Add custom headers/footers with page numbers and dynamic content

```bash
curl --request POST http://localhost:3000/forms/chromium/convert/url \
  --form url=https://example.com \
  --form headerHtml=@header.html \
  --form footerHtml=@footer.html \
  -o output.pdf
```

**Footer Example** (footer.html):
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-size: 10pt; text-align: center; }
  </style>
</head>
<body>
  <span class="pageNumber"></span> / <span class="totalPages"></span>
</body>
</html>
```

**Available Classes**:
- `.date` - Formatted print date
- `.title` - Document title
- `.url` - Document URL
- `.pageNumber` - Current page number
- `.totalPages` - Total page count

**Important**: Use large font sizes and avoid external assets (images, fonts) in headers/footers.

### 7. Webhook for Async Processing

**Description**: Upload generated PDFs to external webhook endpoints asynchronously

```bash
curl --request POST http://localhost:3000/forms/chromium/convert/url \
  --header 'Gotenberg-Webhook-Url: https://my.webhook.url' \
  --header 'Gotenberg-Webhook-Method: PUT' \
  --header 'Gotenberg-Webhook-Error-Url: https://my.error.url' \
  --header 'Gotenberg-Webhook-Error-Method: POST' \
  --header 'Gotenberg-Webhook-Extra-Http-Headers: {"Authorization": "Bearer token123"}' \
  --form url=https://example.com
```

**Response**: `204 No Content` (processing continues in background)

**Webhook Headers**:
- `Gotenberg-Webhook-Url` - Success callback URL
- `Gotenberg-Webhook-Method` - HTTP method (PUT, POST, PATCH)
- `Gotenberg-Webhook-Error-Url` - Error callback URL
- `Gotenberg-Webhook-Extra-Http-Headers` - JSON object with custom headers

### 8. Office Document to PDF

**Description**: Convert Word, Excel, PowerPoint, and other Office formats to PDF

```bash
curl --request POST http://localhost:3000/forms/libreoffice/convert \
  --form files=@document.docx \
  --form files=@spreadsheet.xlsx \
  -o merged.pdf
```

**Supported Extensions** (140+ formats):
- Documents: .doc, .docx, .rtf, .odt, .txt
- Spreadsheets: .xls, .xlsx, .ods, .csv
- Presentations: .ppt, .pptx, .odp
- Images: .png, .jpg, .gif, .bmp, .svg
- PDFs: .pdf (for manipulation/compression)

### 9. PDF Merging

**Description**: Merge multiple PDFs in alphanumeric order

```bash
curl --request POST http://localhost:3000/forms/pdfengines/merge \
  --form files=@file1.pdf \
  --form files=@file2.pdf \
  --form files=@file3.pdf \
  -o merged.pdf
```

**Note**: Alphanumeric order means numbers first, then letters alphabetically.

### 10. Wait for JavaScript Rendering

**Description**: Ensure JavaScript-heavy pages render completely before PDF generation

```bash
# Wait by time delay (3 seconds)
curl --request POST http://localhost:3000/forms/chromium/convert/url \
  --form url=https://react-app.com \
  --form waitDelay=3s \
  -o output.pdf

# Wait for specific JavaScript expression
curl --request POST http://localhost:3000/forms/chromium/convert/url \
  --form url=https://vue-app.com \
  --form waitForExpression="window.appReady === true" \
  -o output.pdf
```

**Best Practice**: Use `waitForExpression` when you control the page code:
```javascript
// In your app
window.appReady = true;  // Signal Gotenberg to render
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Webhook feature for asynchronous PDF uploads, configuration details, error handling, and custom HTTP headers
- **configuration.md** - Complete module configuration guide including API server settings, Chromium options, LibreOffice parameters, PDF engine settings, webhook configuration, Prometheus metrics, logging options, graceful shutdown, and custom fonts
- **modules.md** - Detailed route documentation covering Chromium conversion (URL/HTML/Markdown to PDF), LibreOffice conversion, PDF manipulation (merge/split/flatten), page properties, headers/footers, wait mechanisms, cookies, screenshots, PDF/A conversion, and metadata handling
- **other.md** - Troubleshooting guide for common issues with Chromium (large files, startup problems, blank PDFs, timeouts) and LibreOffice (PDF/A-1a compatibility)

Use the Read tool to explore specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners

**Start Here**:
1. Run Gotenberg locally: `docker run -p 3000:3000 gotenberg/gotenberg:8`
2. Try the basic URL to PDF example above
3. Read `references/modules.md` for route documentation
4. Experiment with page properties (margins, size, orientation)

**Common First Tasks**:
- Convert a web page to PDF
- Add custom headers/footers
- Set paper size and margins
- Handle JavaScript-heavy pages with `waitDelay`

### For Intermediate Users

**Focus Areas**:
- **Custom Templates**: Create HTML templates for Markdown conversion
- **Webhook Integration**: Set up asynchronous processing for production
- **Office Conversions**: Batch convert Office documents
- **PDF Manipulation**: Merge, split, and convert to PDF/A
- **Configuration**: Fine-tune Chromium and LibreOffice settings

**Reference**: `references/configuration.md` for module settings

### For Advanced Users

**Advanced Techniques**:
- **Performance Tuning**: Scale horizontally with multiple Gotenberg instances
- **Custom Fonts**: Build custom Docker images with additional fonts
- **Screenshot Capture**: Use image conversion routes for web screenshots
- **PDF/UA Compliance**: Generate accessible PDFs with tagged structure
- **Network Filtering**: Control resource loading with status code filtering
- **Custom User IDs**: Build images for OpenShift compatibility

**Deep Dive**: `references/api.md` and `references/modules.md`

## Common Patterns

### Environment Variables vs Command Flags

Both approaches work identically:

```bash
# Using command flags
docker run --rm -p "3000:3000" gotenberg/gotenberg:8 \
  gotenberg --my-module-property=foo

# Using environment variables
docker run --rm -p "3000:3000" \
  -e MY_MODULE_PROPERTY=foo \
  gotenberg/gotenberg:8
```

### Trace Header for Request Tracking

```bash
# Custom trace ID
curl --request POST http://localhost:3000/forms/chromium/convert/url \
  --header 'Gotenberg-Trace: my-request-123' \
  --form url=https://example.com \
  -o output.pdf

# Response includes trace
# Gotenberg-Trace: my-request-123
```

### Custom Output Filename

```bash
curl --request POST http://localhost:3000/forms/chromium/convert/url \
  --header 'Gotenberg-Output-Filename: invoice-2024-01' \
  --form url=https://invoice.example.com \
  -o output.pdf

# Generated filename: invoice-2024-01.pdf
```

### PDF/A Conversion for Archival

```bash
# Convert to PDF/A-2b format
curl --request POST http://localhost:3000/forms/chromium/convert/url \
  --form url=https://example.com \
  --form pdfa=PDF/A-2b \
  -o compliant.pdf
```

**Available Formats**: PDF/A-1a, PDF/A-1b, PDF/A-2a, PDF/A-2b, PDF/A-2u, PDF/A-3a, PDF/A-3b, PDF/A-3u

## Troubleshooting Guide

### Large PDF File Sizes

**Problem**: Generated PDFs are larger than expected

**Solutions**:
1. Set `printBackground=false` to exclude background graphics
2. Reduce image quality in source HTML/CSS
3. Use LibreOffice route with compression for Office docs

### Blank PDFs from JavaScript Apps

**Problem**: PDF is blank or incomplete

**Solutions**:
1. Add `waitDelay=3s` to allow rendering time
2. Use `waitForExpression="window.ready === true"`
3. Set `skipNetworkIdleEvent=false` for network-dependent content
4. Check Chromium logs for JavaScript errors

### Webhook Errors

**Error**: `Gotenberg-Trace: {trace}` with error body

**Common Causes**:
1. Unauthorized webhook URL (check `--webhook-allow-list`)
2. Invalid headers in `Gotenberg-Webhook-Extra-Http-Headers`
3. Webhook endpoint unreachable or timing out

**Solution**: Check webhook configuration in `references/configuration.md`

### Timeouts (503 Service Unavailable)

**Problem**: Request times out before completion

**Solutions**:
1. Increase API timeout: `--api-timeout=60s`
2. Reduce content complexity or page count
3. Scale horizontally with multiple Gotenberg instances
4. Use webhook for async processing

## Resources

### Official Documentation
- Main docs: https://gotenberg.dev/docs
- Configuration: https://gotenberg.dev/docs/configuration
- Routes: https://gotenberg.dev/docs/routes

### Docker Hub
- Image: `gotenberg/gotenberg:8`
- Architectures: amd64, arm64, armv7

### Testing Webhooks
- Use [PipeDream](https://pipedream.com) for webhook testing and inspection

## Notes

- **Browser Engine**: All architectures now use Chromium (Google Chrome removed in 8.22.0)
- **Parallel Processing**: Single engine instances cannot process requests in parallel - scale with multiple containers
- **Graceful Shutdown**: Configure `--api-graceful-shutdown` to allow in-flight requests to complete
- **Custom Fonts**: Mount fonts to `/usr/local/share/fonts/` or build custom image
- **Metadata Writing**: May compromise PDF/A compliance - test thoroughly

## Version Info

This skill is based on Gotenberg 8.x documentation. For version-specific features:
- PDF/UA support: 8.21.0+
- Arbitrary user IDs (OpenShift): 8.21.0+
- Chromium auto-restart: 8.15.2+
- GCP logging fields: 8.19.0+
