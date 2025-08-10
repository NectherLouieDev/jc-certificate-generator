# Certificate Generator App

*Generate personalized certificates in bulk from CSV data*

## Features
- 🖼️Create certificates from templates (3KM and 5KM versions)
- 📊 Process multiple names from CSV files
- ✏️ Customize font styles and positioning
- 📁 Export as individual images or combined PDF
- 🖨️ Print-ready output

---

## Installation

### Windows
1. Download the `CertificateGenerator.zip` file
2. Extract to your preferred location
3. Double-click `CertificateGenerator.exe`

![Certificate Generator Folder](screenshots/cert-gen-folder.png)

---

## Quick Start Guide

### 1. Prepare Your Files
- **CSV File** (Required format):  

  ```csv
  Full Name,Registration Type
  John Doe,3KM w/ Certificate
  Jane Smith,5KM w/ T-shirt & Certificate
  ```

- **Template Images**:
  - `3km.jpg` (.jpg extension)
  - `5km.jpg` 

### 2. Launch the App
![Main Interface](screenshots/main-window.png)

### 3. Configure Settings
1. Select your CSV file
2. Choose template images
3. Adjust font settings:
   - Font style (dropdown)
   - Font size (60 recommended)
   - Text position (Y-coordinate)

### 4. Generate Certificates
Click the "Generate Certificates" button and wait for completion.

---

## Output Files
The app creates:
```
/output
  ├── /output_certificates_3km
  │   ├── certificate_John_Doe.jpg
  │   └── certificate_Jane_Smith.jpg
  ├── /output_certificates_5km
  │   └── ...
  ├── 3km_certs.pdf
  └── 5km_certs.pdf
```