with open('frontend/src/pages/UploadReport.tsx', encoding='utf-8') as f:
    c = f.read()

handlers_str = """  const handleCopyTest = (code: string) => {
    navigator.clipboard.writeText(code);
  };

  const handleDownloadTest = (filename: string, code: string) => {
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };
"""

# remove it from where it was
c = c.replace(handlers_str, '')

# there's a dangling "return (" from the previous replacement that failed to insert properly if it was split
# Let's clean up the dangling return if any:
# The previous replace was: c.replace('  return (', handlers + '  return (', 1)
# So if we just replaced handlers_str, there's a dangling '  return ('
# Actually let's just use regex to find the main return and insert the handlers before it.

idx = c.find('return (\n    <div className="min-h-screen')
if idx == -1:
    idx = c.find('return (\n    <div')

if idx != -1:
    c = c[:idx] + handlers_str + '\n  ' + c[idx:]
    with open('frontend/src/pages/UploadReport.tsx', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed!")
else:
    print("Could not find main return")
