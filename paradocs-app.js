// ParaDocs Dynamic Document Index
let allDocuments = [];
let filteredDocuments = [];

// Load documents on page load
window.addEventListener('DOMContentLoaded', () => {
    loadDocuments();
    setupEventListeners();
});

async function loadDocuments() {
    try {
        const response = await fetch('paradocs_all_files.json');
        allDocuments = await response.json();
        filteredDocuments = [...allDocuments];
        
        updateStats();
        populateFilters();
        renderTable();
    } catch (error) {
        console.error('Error loading documents:', error);
        document.getElementById('tableContainer').innerHTML = 
            '<div class="no-results">Error loading documents. Please refresh the page.</div>';
    }
}

function updateStats() {
    // Total documents
    document.getElementById('totalDocs').textContent = allDocuments.length;
    
    // Categories
    const categories = new Set(allDocuments.map(doc => doc.category));
    document.getElementById('totalCategories').textContent = categories.size;
    
    // Total size
    let totalBytes = 0;
    allDocuments.forEach(doc => {
        const match = doc.size.match(/([0-9.]+)\s*(\w+)/);
        if (match) {
            const value = parseFloat(match[1]);
            const unit = match[2];
            const multipliers = { B: 1, KB: 1024, MB: 1024*1024, GB: 1024*1024*1024 };
            totalBytes += value * (multipliers[unit] || 1);
        }
    });
    document.getElementById('totalSize').textContent = formatFileSize(totalBytes);
    
    // File types
    const types = new Set(allDocuments.map(doc => doc.extension));
    document.getElementById('fileTypes').textContent = types.size;
}

function formatFileSize(bytes) {
    const units = ['B', 'KB', 'MB', 'GB'];
    let size = bytes;
    let unitIndex = 0;
    
    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }
    
    return `${size.toFixed(1)} ${units[unitIndex]}`;
}

function populateFilters() {
    // Category filter
    const categories = [...new Set(allDocuments.map(doc => doc.category))].sort();
    const categoryFilter = document.getElementById('categoryFilter');
    categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat.replace(/_/g, ' ');
        categoryFilter.appendChild(option);
    });
    
    // Type filter
    const types = [...new Set(allDocuments.map(doc => doc.extension))].sort();
    const typeFilter = document.getElementById('typeFilter');
    types.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type.toUpperCase();
        typeFilter.appendChild(option);
    });
}

function setupEventListeners() {
    // Search box
    document.getElementById('searchBox').addEventListener('input', filterDocuments);
    
    // Filters
    document.getElementById('categoryFilter').addEventListener('change', filterDocuments);
    document.getElementById('typeFilter').addEventListener('change', filterDocuments);
}

function filterDocuments() {
    const searchTerm = document.getElementById('searchBox').value.toLowerCase();
    const categoryFilter = document.getElementById('categoryFilter').value;
    const typeFilter = document.getElementById('typeFilter').value;
    
    filteredDocuments = allDocuments.filter(doc => {
        // Search filter
        const searchMatch = !searchTerm || 
            doc.filename.toLowerCase().includes(searchTerm) ||
            doc.category.toLowerCase().includes(searchTerm) ||
            (doc.metadata && JSON.stringify(doc.metadata).toLowerCase().includes(searchTerm));
        
        // Category filter
        const categoryMatch = !categoryFilter || doc.category === categoryFilter;
        
        // Type filter
        const typeMatch = !typeFilter || doc.extension === typeFilter;
        
        return searchMatch && categoryMatch && typeMatch;
    });
    
    renderTable();
}

function renderTable() {
    const container = document.getElementById('tableContainer');
    
    if (filteredDocuments.length === 0) {
        container.innerHTML = '<div class="no-results">No documents found matching your criteria.</div>';
        document.getElementById('resultsCount').textContent = 'No results';
        return;
    }
    
    document.getElementById('resultsCount').textContent = 
        `Showing ${filteredDocuments.length} of ${allDocuments.length} documents`;
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th onclick="sortTable('id')">ID ↕</th>
                    <th onclick="sortTable('filename')">Filename ↕</th>
                    <th onclick="sortTable('category')">Category ↕</th>
                    <th onclick="sortTable('extension')">Type ↕</th>
                    <th onclick="sortTable('size')">Size ↕</th>
                    <th onclick="sortTable('date')">Date ↕</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    filteredDocuments.forEach(doc => {
        html += `
            <tr>
                <td>${doc.id}</td>
                <td>${escapeHtml(doc.filename)}</td>
                <td><span class="category-badge">${doc.category.replace(/_/g, ' ')}</span></td>
                <td>${doc.extension.toUpperCase()}</td>
                <td>${doc.size}</td>
                <td>${doc.date}</td>
                <td>
                    <a href="${doc.path}" target="_blank">View</a>
                    ${doc.metadata ? ' | <a href="#" onclick="showMetadata('' + doc.id + '')">Info</a>' : ''}
                </td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

let sortDirection = {};
function sortTable(column) {
    sortDirection[column] = !sortDirection[column];
    
    filteredDocuments.sort((a, b) => {
        let aVal = a[column];
        let bVal = b[column];
        
        if (column === 'size') {
            // Convert to bytes for sorting
            aVal = parseSize(a.size);
            bVal = parseSize(b.size);
        }
        
        if (aVal < bVal) return sortDirection[column] ? -1 : 1;
        if (aVal > bVal) return sortDirection[column] ? 1 : -1;
        return 0;
    });
    
    renderTable();
}

function parseSize(sizeStr) {
    const match = sizeStr.match(/([0-9.]+)\s*(\w+)/);
    if (!match) return 0;
    
    const value = parseFloat(match[1]);
    const unit = match[2];
    const multipliers = { B: 1, KB: 1024, MB: 1024*1024, GB: 1024*1024*1024 };
    
    return value * (multipliers[unit] || 1);
}

function resetFilters() {
    document.getElementById('searchBox').value = '';
    document.getElementById('categoryFilter').value = '';
    document.getElementById('typeFilter').value = '';
    filterDocuments();
}

function exportResults() {
    // Create CSV content
    let csv = 'ID,Filename,Category,Type,Size,Date,Path\n';
    filteredDocuments.forEach(doc => {
        csv += `"${doc.id}","${doc.filename}","${doc.category}","${doc.extension}","${doc.size}","${doc.date}","${doc.path}"\n`;
    });
    
    // Download CSV
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `paradocs_export_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

function showMetadata(docId) {
    const doc = allDocuments.find(d => d.id === docId);
    if (doc && doc.metadata) {
        let info = `Metadata for ${doc.filename}:\n\n`;
        Object.entries(doc.metadata).forEach(([key, value]) => {
            info += `${key}: ${value}\n`;
        });
        alert(info);
    }
}
