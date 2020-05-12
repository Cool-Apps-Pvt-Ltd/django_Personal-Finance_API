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
4. 'django.middleware.csrf.CsrfViewMiddleware' CSRF Validation is disabled [Commit - d9f61ba..ac9c558  master -> master]

# Home Organization Model [GIT Branch Created - setup-organization]
1. Created OrganizationModel in personal_finance_api/models.py
2. Created OrganizationSerializer in personal_finance_api/serializers.py
3. Created OrganizationViewSet in personal_finance_api/views.py
4. Created personal_finance_api/signals.py to handle signals/connectors
5. Added Permissions, TokenAuth for OrgUpdate and OrgGet
6. Created MemberModel personal_finance_api/models.py
7. Created MemberSerializer in personal_finance_api/serializers.py
8. Created MemberViewSet in personal_finance_api/views.py
9. Added connector create_member in personal_finance_api/signals.py to create a member when home org is created
10. Updated personal_finance_api/__init__.py to add signals [Commit - ac9c558..c14ca15  setup-organization -> setup-organization]

# Docker, Travis-ci and flack8
1. Setup Dockerfile and docker-compose.yml [Commit - c14ca15..29bb4f8  setup-organization -> setup-organization]
2. Travis-ci integration added [Commit - 29bb4f8..3b767b5  setup-organization -> setup-organization]
3. Updated docker-compose.yml [Commit - 3b767b5..1ceb562  setup-organization -> setup-organization]
4. Cleaned-up imports across app as Travis-ci test fails [Commit - 1ceb562..63e31f7  setup-organization -> setup-organization]
5. Cleaned-up file formatting [Commit - 63e31f7..2dcd607  setup-organization -> setup-organization]
6. Cleaned-up file formatting [Commit - 2dcd607..2253233  setup-organization -> setup-organization]
7. Cleaned-up file formatting [Commit - 2253233..bac5dcb  setup-organization -> setup-organization]
8. Cleaned-up file formatting [Commit - bac5dcb..264f2a9  setup-organization -> setup-organization]
Travis-ci Test passed successfully till this point

# Writing Unit tests
1. Created personal_finance_api/tests directory for unit tests
2. Added Unit tests for User Creation, Super User creation [Commit - 264f2a9..0f32d04  setup-organization -> setup-organization]
3. Updated personal_finance_api/models.py create_superuser method to return user
4. Updated personal_finance/settings.py to enable DEBUG depending on env variables [Commit - 0f32d04..f56cc1a  setup-organization -> setup-organization]

# Admin Site Tests
1. Create personal_finance_api/tests/tests_admin.py 
2. Added AdminSiteTests class and test_users_listed method to test Admin Site Users
3. Updated personal_finance_api/admin.py to list Users in Admin Site 
4. Added test_user_change_page to personal_finance_api/tests/tests_admin.py to test user profile change in admin [Commit - f56cc1a..c7ee286  setup-organization -> setup-organization]
5. Updated test_admin.py indentation [Commit -  c7ee286..20f627d  setup-organization -> setup-organization]

# Bug Fixes
1. MemberViewSet in personal_finance_api/views.py failure in query_set. Fixed org_id
2. Added URL in personal_finance_api/urls.py for MemberViewSet
3. Fixed UserProfileViewSet in personal_finance_api/views.py  
4. Created OrgMemberUpdate in personal_finance_api/permissions.py 
5. Updated HomeOrgUpdate, UpdateOwnProfile in personal_finance_api/permissions.py
6. Updated Organization, Member Models in personal_finance_api/models.py to add fields
7. Updated Serializers based on point 6
8. Updated personal_finance_api/apps.py to clear indentation [Commit - 20f627d..dcb2215  setup-organization -> setup-organization]
Indentation Fix [Commit - dcb2215..8a86e4e  setup-organization -> setup-organization]
Indentation Fix [Commit - 8a86e4e..52264e1  setup-organization -> setup-organization]
Indentation Fix [Commit - 52264e1..8a8d594  setup-organization -> setup-organization]
Indentation Fix [Commit - 8a8d594..441577a  setup-organization -> setup-organization]
Indentation Fix [Commit - 441577a..9f9cfb5  setup-organization -> setup-organization]
Indentation Fix [Commit - 9f9cfb5..955ab0f  setup-organization -> setup-organization]

# GIT Branch setup-finance-module-app
1. Updated personal_finance_api/permissions.py and personal_finance_api/views.py to allow POST for UserProfile
2. Created new App core_finance_app
3. Updated personal_finance/settings.py to add the app created in '2' to INSTALLED_APPS_LIST
4. Updated personal_finance_api/constants.py to add URL 
5. Updated personal_finance_api/models.py to add URL to Organization Model
6. Updated personal_finance_api/serializers.py to add URL to Organization Serializer

# core_finance_app
1. Created core_finance_app/ serializers.py, constants.py, signals.py
2. Updated core_finance_app/apps.py to connect to signals.py
3. Created Models MonthYear, Income, CurrencyConverter in core_finance_app/models.py
4. Created IncomeSerializer in core_finance_app/serializers.py
5. Created IncomeViewSet in core_finance_app/views.py 
6. Updated core_finance_app/urls.py to add reference to IncomeViewSet
7. Updated personal_finance/urls.py to add reference to core_finance_app [Commit - bceb5a3..ae2d075  setup-finance-module-app -> setup-finance-module-app]
Indentation Fixes [Commit - ae2d075..4bb2676  setup-finance-module-app -> setup-finance-module-app]
Indentation Fixes [Commit - 4bb2676..9eced5a  setup-finance-module-app -> setup-finance-module-app]

- In personal_finance_api App
8. Updated personal_finance_api/permissions.py OrgElementPermissions class to be used across org
9. Updated personal_finance_api/views.py to add CreateUser APIView for user Registration
10. Updated personal_finance_api/urls.py to add API endpoint for 9
11. Updated 'email' to NOTNULL in UserProfileModel personal_finance_api/models.py 

- In core_finance_app
12. Updated IncomeViewSet in core_finance_app/views.py for PUT/PATCH/POST/GET
13. Automation added for IncomeViewSet to account for MonthYear Model
14. Updated core_finance_app/urls.py to add reference to Org Members
15. Updated core_finance_app/urls.py to add create_month_year Connector
16. Created MonthYearSerializer in core_finance_app/serializers.py
17. Updated Income Model in core_finance_app/models.py
18. Created core_finance_app/constants.py [Commit - 9eced5a..b6803d0  setup-finance-module-app -> setup-finance-module-app]
Indentation Fixes [Commit - b6803d0..45bf7e7  setup-finance-module-app -> setup-finance-module-app]

19. Updated Income Model - Indexes, 
20. Created MonthYear Model - Fields total_income, total_deductions, total_tax_withheld
21. Updated MonthYearSerializer to add fields above
22. Removed MemberViewSet URL in personal_finance_api/urls.py
23. Created CurrencyConverter Model, CurrencySerializer and CurrencyViewSet
24. Added to_usd and from_usd_to_primary methods in personal_finance_api/models.py
25. Added Currency URL in personal_finance_api/urls.py
26. Added CurrencyModel to Admin 