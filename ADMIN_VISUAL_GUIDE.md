# CIDE Admin Dashboard - Visual Tour

## 🎯 Quick Access

```
📍 URL: http://localhost:5000/admin
🔐 Username: admin
🔑 Password: admin123
```

---

## 🖼️ Screen Layouts

### 1. Login Page (`/admin`)
```
┌────────────────────────────────────────────┐
│                                            │
│         🛡️  CIDE Admin                     │
│     Code Integrity Detection Engine        │
│                                            │
│     ┌────────────────────────────┐        │
│     │ 👤 Username                │        │
│     │ [___________________]      │        │
│     │                            │        │
│     │ 🔒 Password                │        │
│     │ [___________________]      │        │
│     │                            │        │
│     │ ☐ Remember me              │        │
│     │              Forgot password?       │
│     │                            │        │
│     │   [   🔐 Login   ]        │        │
│     └────────────────────────────┘        │
│                                            │
│        ← Back to Main App                 │
│                                            │
│   ⚠️ Dev Mode: admin / admin123           │
│                                            │
└────────────────────────────────────────────┘
```

---

### 2. Dashboard Overview (`/admin` - authenticated)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  🛡️ CIDE Admin Dashboard                    🏠 Main App  🔓 Logout          │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  📊 STATISTICS CARDS                                                         │
│                                                                              │
│  ┌──────────────────┬──────────────────┬──────────────────┬──────────────┐ │
│  │ 📈 Total         │ 📊 Avg           │ ⚠️  High Risk    │ 📁 Files     │ │
│  │ Analyses         │ Similarity       │ (>80%)           │ Analyzed     │ │
│  │                  │                  │                  │              │ │
│  │   42             │   65.2%          │   8              │   102        │ │
│  │ ↑ 12.5% growth   │ Stable           │ Potential issues │ Total count  │ │
│  └──────────────────┴──────────────────┴──────────────────┴──────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  📈 CHARTS                                                                   │
│                                                                              │
│  ┌─────────────────────────────────────┬──────────────────────────────────┐ │
│  │ 📊 Analysis Trend (Last 7 Days)     │ 💻 Language Distribution         │ │
│  │                                     │                                  │ │
│  │      ●                              │         ╱───╲                    │ │
│  │     ╱ ╲        ●                    │       ╱       ╲                  │ │
│  │    ╱   ╲      ╱ ╲                  │     ╱           ╲                │ │
│  │   ●     ●────●   ●───●              │    │  Python 60%  │               │ │
│  │ ──┴─────┴─────┴─────┴──            │    │  Java   25%  │               │ │
│  │ 24  25  26  27  28  29  30         │    │  JS     15%  │               │ │
│  │                                     │     ╲           ╱                │ │
│  └─────────────────────────────────────┴──────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  🔍 FILTERS                                                                  │
│                                                                              │
│  Search: [__________]  Language: [All ▼]  Risk: [All ▼]  Date: [All Time ▼]│
│  [Apply Filters] [Reset]                                  [⬇ Export CSV]    │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  📜 ANALYSIS HISTORY                                        🔄 Refresh       │
│                                                                              │
│  ┌──────────────┬──────────────┬──────────┬──────┬────────┬──────┬────────┐│
│  │ Timestamp ▲  │ Files        │ Language │ Mode │ Simil. │ Risk │ Actions││
│  ├──────────────┼──────────────┼──────────┼──────┼────────┼──────┼────────┤│
│  │ 2025-01-30   │ file1.py,... │ Python   │ Hyb  │ 85.3%  │ High │ 👁️ 🗑️  ││
│  │ 14:23:45     │              │          │      │        │      │        ││
│  ├──────────────┼──────────────┼──────────┼──────┼────────┼──────┼────────┤│
│  │ 2025-01-30   │ test1.java...│ Java     │ AST  │ 72.1%  │ Med  │ 👁️ 🗑️  ││
│  │ 13:15:22     │              │          │      │        │      │        ││
│  ├──────────────┼──────────────┼──────────┼──────┼────────┼──────┼────────┤│
│  │ 2025-01-30   │ script.js,...│ JS       │ Basic│ 42.8%  │ Low  │ 👁️ 🗑️  ││
│  │ 12:08:11     │              │          │      │        │      │        ││
│  ├──────────────┼──────────────┼──────────┼──────┼────────┼──────┼────────┤│
│  │ 2025-01-29   │ main.cpp,... │ C++      │ AST  │ 91.5%  │ High │ 👁️ 🗑️  ││
│  │ 16:42:33     │              │          │      │        │      │        ││
│  └──────────────┴──────────────┴──────────┴──────┴────────┴──────┴────────┘│
│                                                                              │
│  Showing 1 to 10 of 42 results            [◀] Page 1 [▶]                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Color Scheme

### Risk Level Badges
```
🟢 Low    (0-50%)   : Green badge  - #d1fae5
🟡 Medium (50-80%)  : Orange badge - #fed7aa
🔴 High   (80-100%) : Red badge    - #fecaca
```

### Chart Colors
```
📊 Line Chart:  Blue gradient (#3b82f6)
🍩 Donut Chart: Blue, Purple, Green, Orange, Red
```

### Card Icons
```
📈 Total Analyses   : Blue (#3b82f6)
📊 Avg Similarity   : Purple (#9333ea)
⚠️  High Risk       : Red (#dc2626)
📁 Files Analyzed   : Green (#16a34a)
```

---

## 🎬 User Flow

### Logging In
```
1. Navigate to /admin
   ↓
2. See login page
   ↓
3. Enter credentials (admin/admin123)
   ↓
4. Click "Login"
   ↓
5. Redirected to dashboard
```

### Filtering Data
```
1. Type filename in search: "test"
   ↓
2. Select language: "Python"
   ↓
3. Select risk: "High (80-100%)"
   ↓
4. Select date: "Last 7 Days"
   ↓
5. Click "Apply Filters"
   ↓
6. Table updates instantly
```

### Exporting Data
```
1. Apply filters (optional)
   ↓
2. Click "Export CSV"
   ↓
3. File downloads: cide_analyses_2025-01-30.csv
   ↓
4. Open in Excel/Google Sheets
```

### Viewing Details
```
1. Find analysis in table
   ↓
2. Click 👁️ (View) icon
   ↓
3. Redirected to /admin/analysis/42
   ↓
4. See full analysis details
```

### Deleting Analysis
```
1. Find analysis in table
   ↓
2. Click 🗑️ (Delete) icon
   ↓
3. Confirm deletion
   ↓
4. Record removed from database
   ↓
5. Table refreshes automatically
```

---

## 📱 Responsive Design

### Desktop (1920x1080)
```
┌────────────────────────────────────────────────────────────┐
│  [4 cards in row] [2 charts side by side] [Full table]    │
└────────────────────────────────────────────────────────────┘
```

### Tablet (768x1024)
```
┌──────────────────────────────┐
│  [2 cards per row]           │
│  [Charts stacked]            │
│  [Scrollable table]          │
└──────────────────────────────┘
```

### Mobile (375x667)
```
┌────────────────┐
│  [1 card]      │
│  [1 card]      │
│  [Chart]       │
│  [Chart]       │
│  [Table cards] │
└────────────────┘
```

---

## 🔥 Hot Features

### 1. Real-Time Updates
```javascript
// Auto-refresh every 30 seconds
setInterval(loadAnalyses, 30000);
```

### 2. Instant Search
```javascript
// Search updates as you type
searchInput.addEventListener('input', applyFilters);
```

### 3. Sortable Columns
```javascript
// Click any column header to sort
onclick="sortTable('timestamp')"
```

### 4. Smart Pagination
```javascript
// Navigate through pages
[◀ Previous] [Page 1] [Next ▶]
```

---

## 🛠️ Admin Tasks

### Daily Tasks
- [ ] Check high-risk analyses (>80% similarity)
- [ ] Review new analyses since yesterday
- [ ] Export weekly report (CSV)
- [ ] Monitor language distribution trends

### Weekly Tasks
- [ ] Analyze trend chart for patterns
- [ ] Delete old/irrelevant analyses
- [ ] Check growth metrics
- [ ] Update risk thresholds if needed

### Monthly Tasks
- [ ] Generate monthly statistics report
- [ ] Review average similarity trends
- [ ] Optimize database (when implemented)
- [ ] Backup analysis data

---

## 🚨 Alert Scenarios

### High Risk Detection
```
When similarity > 80%:
- Red badge displayed
- Appears in "High Risk" count
- Admin should investigate
```

### Usage Spike
```
When analyses > 20/day:
- Growth percentage increases
- Trend chart shows spike
- May indicate batch processing
```

### No Recent Activity
```
When no analyses today:
- "Today" filter shows 0 results
- Trend chart shows flat line
- May indicate downtime
```

---

## 💡 Pro Tips

### Keyboard Shortcuts (Planned)
```
Ctrl + F    : Focus search
Ctrl + R    : Refresh data
Ctrl + E    : Export CSV
Esc         : Clear filters
```

### Quick Filters
```
High Risk: Click "High Risk" card → Auto-filter >80%
Today:     Click "Growth" → Auto-filter to today
```

### Export Tips
```
1. Filter first, then export (only exports filtered data)
2. Use descriptive filters for report organization
3. Regular exports = backup strategy
```

---

## 📊 Sample Data

### CSV Export Format
```csv
Timestamp,Files,Language,Mode,Similarity,Risk Level
2025-01-30 14:23:45,"file1.py, file2.py",python,hybrid,85.3%,High
2025-01-30 13:15:22,"test1.java, test2.java",java,ast,72.1%,Medium
2025-01-30 12:08:11,"script.js, app.js",javascript,basic,42.8%,Low
```

### JSON API Response
```json
{
  "success": true,
  "analyses": [
    {
      "id": 1,
      "timestamp": "2025-01-30 14:23:45",
      "files": "file1.py, file2.py",
      "language": "python",
      "mode": "hybrid",
      "similarity": 85.3,
      "file_count": 2
    }
  ]
}
```

---

## 🔐 Security Notes

### Current (Development)
```
✅ Session-based auth
✅ Environment variables
⚠️  Plain text passwords
⚠️  In-memory storage
⚠️  No rate limiting
```

### Production (TODO)
```
🔒 Bcrypt password hashing
🔒 PostgreSQL database
🔒 Rate limiting (10 req/min)
🔒 HTTPS only
🔒 CSRF protection
```

---

## 🎯 Success Metrics

### Good Health Indicators
```
✅ Average similarity: 30-60% (normal range)
✅ High risk count: <10% of total
✅ Steady growth: 5-15% weekly
✅ Language diversity: Multiple languages used
```

### Warning Signs
```
⚠️  Average similarity >70%: Many similar files
⚠️  High risk count >25%: Potential plagiarism wave
⚠️  No growth: System not being used
⚠️  Single language only: Limited use case
```

---

## 📞 Support

### Common Issues

**Q: Can't login?**
```
A: Check credentials (admin/admin123)
   Clear browser cookies
   Check server logs
```

**Q: No data showing?**
```
A: Run some analyses first (/analyze or /batch)
   Click "Refresh" button
   Check browser console for errors
```

**Q: Charts not rendering?**
```
A: Check Chart.js loaded (network tab)
   Clear browser cache
   Try different browser
```

**Q: Export not working?**
```
A: Ensure data is filtered/loaded
   Check pop-up blocker
   Try different browser
```

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Email alerts for high-risk detections
- [ ] Scheduled reports (daily/weekly/monthly)
- [ ] Multi-user support with roles
- [ ] Advanced analytics dashboard
- [ ] Machine learning insights
- [ ] API token management
- [ ] Webhook integrations
- [ ] Dark mode toggle

---

**Visual Guide Version:** 1.0  
**Last Updated:** January 30, 2025  
**CIDE Version:** 2.0  

---

*For technical documentation, see `ADMIN_DASHBOARD.md`*
*For API documentation, see API section in `ADMIN_DASHBOARD.md`*
