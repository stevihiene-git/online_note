
# Check what's in your project directory
echo "Current directory: $(pwd)"
echo "Root level templates: $(ls -d templates/ 2>/dev/null && echo 'Exists' || echo 'Missing')"
echo "Note_app templates: $(ls -d note_app/templates/ 2>/dev/null && echo 'Exists' || echo 'Missing')"
echo "Home.html location: $(find . -name "home.html" -type f 2>/dev/null || echo 'Not found')"



