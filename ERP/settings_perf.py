from .settings_development import *


REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'Core.utils.renderers.BrowsableAPIWithoutFormRenderer',
)
