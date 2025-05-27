# Dashboard Issues Report - ParaDocs Project

Generated: 2025-01-27

## Summary

After repository flattening (removal of `paradocs-agent/` subfolder), several dashboard HTML files contain broken references. The analysis found:

- **Total HTML files scanned**: 67
- **Files with issues**: 2 files with broken paths
- **Files with external dependencies**: 10+ files
- **Critical issues**: 4 broken PDF links in CORRECTED_MASTER_INDEX_VERIFIED.html

## Broken References Found

### 1. CORRECTED_MASTER_INDEX_VERIFIED.html

**Issue**: References to non-existent `paradocs-agent/downloaded/` directory

**Line 226**: 
```html
<a href="paradocs-agent/downloaded/eeoc%20complaint%20signed-rev1-min-bookmarked_compressed.pdf">View PDF</a>
```
**Fix**: Update to `downloaded/eeoc%20complaint%20signed-rev1-min-bookmarked_compressed.pdf`

**Line 236**:
```html
<a href="paradocs-agent/downloaded/LOA%20HS-FEMA-02430-2024.pdf">View PDF</a>
```
**Fix**: Update to `downloaded/LOA%20HS-FEMA-02430-2024.pdf`

**Line 246**:
```html
<a href="paradocs-agent/downloaded/">View ROI Folder</a>
```
**Fix**: Update to `downloaded/`

**Line 256**:
```html
<a href="paradocs-agent/downloaded/Election%20Letter%20-%20HS-FEMA-02430-2024.pdf">View PDF</a>
```
**Fix**: Update to `downloaded/Election%20Letter%20-%20HS-FEMA-02430-2024.pdf`

### 2. JavaScript File References (Working but noted)

**paradocs-index.html** (Line 193):
- References `paradocs-app.js` ✓ (File exists)
- `paradocs-app.js` fetches `paradocs_all_files.json` ✓ (File exists)

**paradocs-enhanced.html** (Line 303):
- References `paradocs-enhanced.js` ✓ (File exists)
- Contains inline data, no external fetches

**paradocs_comprehensive_eeo_investigation.html** (Line 292):
- Fetches `eeo_comprehensive_investigation.json` ✓ (File exists)

## External Dependencies (CDN - Working)

The following files use external CDN resources (Bootstrap, Chart.js, etc.) which should continue working:

1. **paradocs_master_timeline_enhanced.html**
   - Bootstrap CSS/JS (cdn.jsdelivr.net)

2. **paradocs_master_dashboard.html**
   - Bootstrap CSS/JS (cdn.jsdelivr.net)

3. **paradocs_legal_strategy_dashboard.html**
   - Bootstrap CSS/JS (cdn.jsdelivr.net)

4. **paradocs_comprehensive_eeo_investigation.html**
   - Bootstrap CSS/JS (cdn.jsdelivr.net)

5. **paradocs-enhanced.html**
   - Bootstrap CSS/JS (cdn.jsdelivr.net)

6. **MASTER_INDEX.html**
   - Bootstrap CSS/JS (cdn.jsdelivr.net)

7. **GAMMA_APP_PRESENTATION.html**
   - Tailwind CSS (cdn.tailwindcss.com)
   - Chart.js (cdn.jsdelivr.net)

## Internal Link References (Working)

Many dashboards reference other HTML files in the same directory:

- **UNIFIED_PARADOCS_DASHBOARD.html** → Links to multiple other dashboards
- **MASTER_INDEX.html** → Links to JSON data files and other dashboards
- **paradocs_dashboard.html** → Links to config files and scripts

These should continue working after the flattening.

## Recommendations

1. **Apply the fix_dashboard.diff patch** to correct the 4 broken references
2. **Verify the `downloaded/` directory exists** with the referenced PDF files
3. **Consider creating redirects** from old paths to new paths for backward compatibility
4. **Test all dashboards** after applying the patch to ensure functionality

## Files Requiring Fixes

1. `CORRECTED_MASTER_INDEX_VERIFIED.html` - 4 broken links to fix

All other dashboard files appear to be functioning correctly with their current references. 