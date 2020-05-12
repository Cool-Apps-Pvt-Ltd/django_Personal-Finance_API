from calendar import month_name
from rest_framework import viewsets, status, filters, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from personal_finance_api import permissions
from personal_finance_api.models import MemberModel, OrganizationModel
from .models import Income, MonthYear, CurrencyConverter
from .serializers import IncomeSerializer, MonthYearSerializer, \
    CurrencySerializer

"""
1. is_valid_member_in_org
 - Given MemberID and OrgID, method validates if a member belongs to the org

2. IncomeViewSet
 - Validation for Members within OrgID added
 - POST/PUT Added. Validation added Month-Year-Org in MonthYear Model
 - For PATCH, Validation added for MM-YY-Org and for existing data
 - Search fields added for Month and Year
 
3. MonthYearViewSet
 - GET Custom Method Added. Returns months in an org
 - GET/PUT/POST/PATCH allowed. DELETE is disabled for all users
 
4. CurrencyViewSet
 - GET Added to return entries in an org
 - POST/PUT Added. Validation NOT to be added for MonthYear Object
 - Search fields added for Month and Year

@todo
3. MonthYearViewSet
 - Detail GET doesnt work.
 - Need to audit and clear MonthYear Objects with no data

"""


def is_valid_member_in_org(member_id, org_id):
    """Validates if a member belongs to the org"""
    members = MemberModel.objects.filter(org=org_id)
    return member_id in [member.id for member in members]


class IncomeViewSet(viewsets.ModelViewSet):
    """API ViewSet for Income Model"""
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.OrgElementPermissions,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('month', 'year')

    def get_queryset(self):
        """GET Income Transactions in an org"""
        return super().get_queryset().filter(org=self.kwargs['org_id'])

    def perform_create(self, serializer, *args, **kwargs):
        """Override POST method for Income model"""
        try:
            mmyy_is_locked = False
            try:
                mm = serializer.validated_data['month']
                yy = serializer.validated_data['year']
                month_year = MonthYear.objects.get(
                    org=self.kwargs['org_id'],
                    year=yy,
                    month=mm)
                mmyy_is_locked = month_year.is_locked
            except Exception as e:
                print(e)
                pass
            # If MonthYear exists and is locked
            if mmyy_is_locked:
                return super().permission_denied(
                    self.request, 'CAN\'T Create! Locked Month')

            else:
                # Validate if Member is a part of the Org
                if is_valid_member_in_org(
                        serializer.validated_data['member'].id,
                        self.kwargs['org_id']):
                    org_object = OrganizationModel.objects. \
                        get(id=self.kwargs['org_id'])
                    super().perform_create(serializer.save(org=org_object))
                else:
                    super().permission_denied(
                        self.request, 'Invalid Request. Permission Denied!')

        except Exception as e:
            return super().permission_denied(self.request, e)

    def update(self, request, *args, **kwargs):
        """Override PUT method for Income model"""

        try:
            org = OrganizationModel.objects.get(id=self.kwargs['org_id'])
            month_year = MonthYear.objects.get_or_create(
                month=request.data['month'],
                year=request.data['year'],
                org=org)
            # Get MMYY Object
            month_year = month_year[0]

            # If MonthYear exists and is locked
            if month_year.is_locked:
                response = {
                    'Message': 'CAN\'T modify! Month is locked!' +
                               month_name(month_year.month) +
                               str(month_year.year)
                }
                return Response(response,
                                status=status.HTTP_403_FORBIDDEN)
            else:
                # PUT if MonthYear is not locked
                # check if Member belongs to Org
                if is_valid_member_in_org(int(request.data['member']),
                                          self.kwargs['org_id']):
                    return super().update(request, *args, **kwargs)
                else:
                    response = {'Message': "Invalid Request", }
                    return Response(response,
                                    status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(e, status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        """PATCH for Income model"""
        try:
            org = OrganizationModel.objects.get(id=self.kwargs['org_id'])
            current_income_object = Income.objects.get(id=self.kwargs['pk'])

            # PATCH may or may not have certain required fields
            member = current_income_object.member.id
            month = current_income_object.month
            year = current_income_object.year
            if 'member' in request.data:
                member = request.data['member']
            if 'month' in request.data:
                month = request.data['month']
            if 'year' in request.data:
                year = request.data['year']

            request.data['member'] = member
            request.data['month'] = month
            request.data['year'] = year
            request.data['org'] = self.kwargs['org_id']

            # GET or CREATE MonthYear Object
            month_year = MonthYear.objects.get_or_create(month=month,
                                                         year=year,
                                                         org=org)
            # Get MMYY Object
            month_year = month_year[0]

            # If MonthYear exists and is locked
            if month_year.is_locked:
                response = {
                    'Message': 'CAN\'T modify! Month is locked!' +
                               month_name(month_year.month) +
                               str(month_year.year)
                }
                return Response(response,
                                status=status.HTTP_403_FORBIDDEN)
            else:
                # PUT if MonthYear is not locked
                # check if Member belongs to Org
                if is_valid_member_in_org(int(request.data['member']),
                                          self.kwargs['org_id']):

                    return super().update(request, *args, **kwargs)
                else:
                    response = {'Message': "Invalid Request", }
                    return Response(response,
                                    status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(e, status=status.HTTP_401_UNAUTHORIZED)


class MonthYearViewSet(viewsets.ModelViewSet):
    """API ViewSet for MonthYear Model - GET Only"""
    queryset = MonthYear.objects.all()
    serializer_class = MonthYearSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.OrgElementPermissions,)
    http_method_names = ['get', 'put', 'post', 'patch']

    def get_queryset(self):
        """GET MonthYear Objects in an org"""
        return super().get_queryset().filter(org=self.kwargs['org_id'])


class CurrencyViewSet(viewsets.ModelViewSet):
    """API ViewSet for Currency Model"""
    queryset = CurrencyConverter.objects.all()
    serializer_class = CurrencySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.OrgElementPermissions,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('month', 'year')

    def get_queryset(self):
        """GET Currency Transactions in an org"""
        return super().get_queryset().filter(org=self.kwargs['org_id'])

    def perform_create(self, serializer, *args, **kwargs):
        """Override POST method for CurrencyConverter model"""
        # This does not create MonthYear Object if it doesnt exist
        try:
            mmyy_is_locked = False
            try:
                mm = serializer.validated_data['month']
                yy = serializer.validated_data['year']
                month_year = MonthYear.objects.get(
                    org=self.kwargs['org_id'],
                    year=yy,
                    month=mm)
                mmyy_is_locked = month_year.is_locked
            except Exception as e:
                print(e)
                pass

            # If MonthYear doesn't exist or
            # If MonthYear is not locked, create entry
            if mmyy_is_locked:
                return super().permission_denied(
                    self.request, 'CAN\'T Create! Locked Month')
            else:
                org_object = OrganizationModel.objects. \
                    get(id=self.kwargs['org_id'])
                super().perform_create(serializer.save(org=org_object))

        except Exception as e:
            return super().permission_denied(self.request, e)
