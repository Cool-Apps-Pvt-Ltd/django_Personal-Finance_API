# PersonalFinance REST API

PersonalFinance REST API Project

# Project Setup
1. Installed django, djangorestframework
2. Created the project personal_finance
3. Created the app personal_finance_api
4. Updated personal_finance/settings.py with the applications. [Commit - 3d0d965..9bb173d  master -> master]

# User Profile Model
1. Created User Profile Model, Manager in personal_finance_api/models.py [Commit - 9bb173d..46133a0  master -> master]
2. Registered User Profile in Admin View in personal_finance_api/admin.py [Commit - 46133a0..b75ac74  master -> master]
3. Created and tested super users.

# API Views Creation and Testing
1. Created personal_finance_api/urls.py and updated path to this in personal_finance/urls.py 
2. Created User Profile API View - GET/PUT/POST/DELETE/PATCH Methods [Commit - b75ac74..3f9a314  master -> master]
3. Created UserProfileViewSet and Overrode Create method. Removed reference to User Profile API View in the URLs.
4. Added Authentication to UserProfileViewSet to permit users to edit/delete their own profile.
5. Created personal_finance_api/permissions.py with UpdateOwnProfile Class. 
6. Updated UserProfileViewSet to use permissions method UpdateOwnProfile [Commit - 3f9a314..a4b67bf  master -> master]

# User Profile Search 
1. Added Filters in personal_finance_api/views.py 
2. Updated UserProfileViewSet to search with Users with Last Name and Email [Commit - a4b67bf..d9f61ba  master -> master]

# User Login
1. Removed UserProfileApiView from personal_finance_api/views.py as testing is complete
2. Created LoginApiView in personal_finance_api/views.py to allow user login. Users can update profile if logged in, using the token. 
3. Updated personal_finance_api/urls.py to enable Login Endpoint 
4. 'django.middleware.csrf.CsrfViewMiddleware' CSRF Validation is disabled 