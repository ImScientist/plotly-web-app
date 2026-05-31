from plotly_web_app.content import DEFAULT_CONTENT_DIR
from plotly_web_app.preprocess import create_content


if __name__ == '__main__':
    """ Create preprocessed content that will be loaded by the dash app.
    
    Example: 
        python create_content.py
    """
    create_content(str(DEFAULT_CONTENT_DIR))
