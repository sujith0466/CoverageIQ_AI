import re

with open("frontend/src/pages/UploadReport.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add useNavigate
if "useNavigate" not in content:
    content = content.replace(
        "import React, { useState, useRef, useMemo } from 'react';",
        "import React, { useState, useRef, useMemo } from 'react';\nimport { useNavigate } from 'react-router-dom';"
    )

if "const navigate = useNavigate();" not in content:
    content = content.replace(
        "export default function UploadReport() {",
        "export default function UploadReport() {\n  const navigate = useNavigate();"
    )

# Remove Dashboard state
content = re.sub(r"  const \[isLoadingDashboard.*?;\n", "", content)
content = re.sub(r"  const \[dashboardResult.*?;\n", "", content)
content = re.sub(r"  const \[viewMode.*?;\n", "", content)

# Modify handleLoadDashboard
if "handleLoadDashboard" in content:
    content = re.sub(
        r"  const handleLoadDashboard = async \(\) => \{[\s\S]*?\};\n",
        """  const handleLoadDashboard = () => {
    navigate('/dashboard');
  };
""",
        content
    )

# Save to local storage after upload
if "setUploadResult(res);" in content and "localStorage.setItem('latestReportId'" not in content:
    content = content.replace(
        "setUploadResult(res);\n    setIsUploading(false);\n    \n    if (res.success) {\n      setFile(null);\n    }",
        "setUploadResult(res);\n    setIsUploading(false);\n    \n    if (res.success && res.report_id) {\n      localStorage.setItem('latestReportId', res.report_id);\n      setFile(null);\n    }"
    )

# Remove ExecutiveDashboard view markup
if "{viewMode === 'dashboard' && dashboardResult?.success && (" in content:
    content = re.sub(
        r"      \{viewMode === 'dashboard' && dashboardResult\?\.success && \([\s\S]*?\n      \}\)\n",
        "",
        content
    )

# Remove viewMode wrapper around workflow
if "{viewMode === 'workflow' && (" in content:
    content = content.replace("{viewMode === 'workflow' && (<div className=\"max-w-4xl mx-auto space-y-6\">", "<div className=\"max-w-4xl mx-auto space-y-6\">")
    # need to remove the closing )} which is at the very end. Let's just remove `      )}\n` before the last `    </div>\n  );\n}`
    content = re.sub(r"      \)\}\n(    </div>\n  \);\n\})", r"\1", content)
    
# Remove LayoutDashboard import if present
# But LayoutDashboard is used for the "Executive Dashboard" button
# The button text just says "Executive Dashboard", let's keep it.

# Update button to not use isLoadingDashboard
if "disabled={isLoadingDashboard}" in content:
    content = content.replace("disabled={isLoadingDashboard}", "")
    content = content.replace("{isLoadingDashboard ? <Loader2 className=\"animate-spin\" size={20} /> : <LayoutDashboard size={20} />}", "<LayoutDashboard size={20} />")

with open("frontend/src/pages/UploadReport.tsx", "w", encoding="utf-8") as f:
    f.write(content)
