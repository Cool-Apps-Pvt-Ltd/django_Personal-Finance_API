# PersonalFinance REST API

PersonalFinance REST API Project

# Project Setup
1. Installed django, djangorestframework
2. Created the project personal_finance
3. Created the app personal_finance_api
4. Updated personal_finance/settings.py with the applications. (Commit - 3d0d965..9bb173d  master -> master)

# User Profile
1. Created User Profile Model, Manager in personal_finance_api/models.py (Commit - 9bb173d..46133a0  master -> master)
2. Registered User Profile in Admin View in personal_finance_api/admin.py (Commit - 46133a0..b75ac74  master -> master)
3. Created and tested super users.

# API Views
1. Created personal_finance_api/urls.py and updated path to this in personal_finance/urls.py 
2. Created User Profile API View - GET/PUT/POST/DELETE/PATCH Methods (Commit - b75ac74..3f9a314  master -> master)
3. Created UserProfileViewSet and Overrode Create method. Removed reference to User Profile API View in the URLs.
4. Added Authentication to UserProfileViewSet to permit users to edit/delete their own profile.
5. Created personal_finance_api/permissions.py with UpdateOwnProfile Class. 
6. Updated UserProfileViewSet to use permissions method UpdateOwnProfile