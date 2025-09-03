
python3 -c "
from note_app import create_app
app = create_app()
with app.app_context():
    print('Static folder:', app.static_folder)
    import os
    css_path = os.path.join(app.static_folder, 'css', 'style.css')
    print('CSS path:', css_path)
    print('CSS exists:', os.path.exists(css_path))
"
