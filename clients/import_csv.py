from io import TextIOWrapper
import csv
from django.shortcuts import redirect
from django.utils.dateparse import parse_date
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from .models import Client, InternetDetails, InsuranceDetails, TrackingDetails, ServicePlan, UserGroup, Address
from user_authen.models import CustomUser


@csrf_exempt
def import_clients_csv(request):
    if request.method != 'POST' or 'file' not in request.FILES:
        return redirect('clients:client_list')

    file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
    reader = csv.DictReader(file)

    with transaction.atomic():
        for row in reader:
            try:
                # 1. Parse current address
                current_address = Address.objects.create(
                    city=row.get('city', '').strip(),
                    province=row.get('province', '').strip(),
                    district=row.get('district', '').strip(),
                    ward_no=row.get('ward_no', '').strip(),
                    street_name=row.get('street_name', '').strip()
                )

                # 2. Parse permanent address
                perma_address = Address.objects.create(
                    city=row.get('perma_city', '').strip(),
                    province=row.get('perma_province', '').strip(),
                    district=row.get('perma_district', '').strip(),
                    ward_no=row.get('perma_ward_no', '').strip(),
                    street_name=row.get('perma_street_name', '').strip()
                )

                # 3. Basic Client data
                client_data = {
                    'first_name': row.get('first_name', '').strip(),
                    'last_name': row.get('last_name', '').strip(),
                    'dob': parse_date(row.get('dob')) if row.get('dob') else None,
                    'gender': row.get('gender', '').strip(),
                    'nationality': row.get('nationality', '').strip(),
                    'zip': row.get('zip', '').strip(),
                    'country': row.get('country', '').strip(),
                    'phone_number': row.get('phone_number', '').strip(),
                    'email': row.get('email', '').strip(),
                    'vat_pan': row.get('vat_pan', '').strip(),
                    'nid_citizen': row.get('nid_citizen', '').strip(),
                    'passport_number': row.get('passport_number', '').strip(),
                    'company_name': row.get('company_name', '').strip(),
                    'unique_id': row.get('unique_id', '').strip()
                }

                agent = CustomUser.objects.filter(email=row.get('agent')).first()
                billed_by = CustomUser.objects.filter(email=row.get('billed_by')).first()
                created_by = CustomUser.objects.filter(email=row.get('created_by')).first()

                client = Client.objects.create(
                    agent=agent,
                    billed_by=billed_by,
                    created_by=created_by,
                    address=current_address,
                    perma_address=perma_address,
                    **client_data
                )

                # 4. Optional InternetDetails
                if row.get('username_or_mac'):
                    service_plan = ServicePlan.objects.filter(name=row.get('service_plan')).first()
                    user_group = UserGroup.objects.filter(name=row.get('user_group')).first()

                    InternetDetails.objects.create(
                        customer=client,
                        username_or_mac=row['username_or_mac'],
                        enable=row.get('enable', 'True').lower() == 'true',
                        mac_user=row.get('mac_user', 'False').lower() == 'true',
                        password=row.get('password', ''),
                        mac_address_of_cm=row.get('mac_address_of_cm', ''),
                        simultaneous_use=int(row.get('simultaneous_use', 1)),
                        service_plan=service_plan,
                        user_group=user_group,
                        download_limit=int(row.get('download_limit', 0)),
                        upload_limit=int(row.get('upload_limit', 0)),
                        total_limit=int(row.get('total_limit', 0)),
                        account_expiry_date=parse_date(row.get('account_expiry_date')) if row.get('account_expiry_date') else None,
                        radius_comments=row.get('radius_comments', ''),
                        radius_attribute=row.get('radius_attribute', '')
                    )

                # 5. Optional InsuranceDetails
                if 'insurance_comments' in row:
                    InsuranceDetails.objects.create(
                        customer=client,
                        insurance_comments=row.get('insurance_comments', '')
                    )

                # 6. Optional TrackingDetails
                if 'travel_from' in row:
                    TrackingDetails.objects.create(
                        customer=client,
                        travel_from=row['travel_from'],
                        emergency_contact=row.get('emergency_contact', ''),
                        package=row.get('package', ''),
                        travel_start_date=parse_date(row.get('travel_start_date')) if row.get('travel_start_date') else None,
                        travel_end_date=parse_date(row.get('travel_end_date')) if row.get('travel_end_date') else None
                    )

            except Exception as e:
                print(f"[ERROR ROW] {row}\n[ERROR] {e}")
                continue  # Optionally collect these for reporting

    return redirect('client_list')


from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def download_sample_csv(request):
    csv_type = request.GET.get('type', 'client_only')

    # Base Client fields
    client_fields = [
        'first_name', 'last_name', 'dob', 'gender', 'nationality',
        'zip', 'country', 'phone_number', 'email', 'vat_pan', 'nid_citizen',
        'passport_number', 'company_name', 'unique_id', 'agent', 'billed_by', 'created_by',
        # Address (current)
        'city', 'province', 'district', 'ward_no', 'street_name',
        # Permanent address
        'perma_city', 'perma_province', 'perma_district', 'perma_ward_no', 'perma_street_name'
    ]

    internet_fields = [
        'username_or_mac', 'password', 'enable', 'mac_user', 'simultaneous_use',
        'service_plan', 'user_group', 'download_limit', 'upload_limit',
        'total_limit', 'account_expiry_date', 'radius_comments', 'radius_attribute'
    ]

    tracking_fields = [
        'travel_from', 'emergency_contact', 'package',
        'travel_start_date', 'travel_end_date'
    ]

    insurance_fields = ['insurance_comments']

    headers_map = {
        'client_only': client_fields,
        'client_internet': client_fields + internet_fields,
        'client_tracking': client_fields + tracking_fields,
        'client_internet_tracking': client_fields + internet_fields + tracking_fields,
        'client_full': client_fields + internet_fields + tracking_fields + insurance_fields,
    }

    headers = headers_map.get(csv_type, client_fields)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=sample_{csv_type}.csv'

    writer = csv.writer(response)
    writer.writerow(headers)

    return response


def download_csv(request):
    user = request.user

    # Admin sees all, others see only their own clients
    if getattr(user, 'role', '') == 'admin':
        clients = Client.objects.all()
    else:
        clients = Client.objects.filter(created_by=user)

    clients = clients.select_related('address', 'perma_address', 'agent', 'billed_by', 'created_by')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=clients.csv'

    writer = csv.writer(response)

    headers = [
        'first_name', 'last_name', 'dob', 'gender', 'nationality',
        'zip', 'country', 'phone_number', 'email', 'vat_pan', 'nid_citizen',
        'passport_number', 'company_name', 'unique_id',
        'agent', 'billed_by', 'created_by',
        'city', 'province', 'district', 'ward_no', 'street_name',
        'perma_city', 'perma_province', 'perma_district', 'perma_ward_no', 'perma_street_name',
    ]
    writer.writerow(headers)

    for client in clients:
        addr = client.address
        paddr = client.perma_address
        writer.writerow([
            client.first_name, client.last_name, client.dob, client.gender, client.nationality,
            client.zip, client.country, client.phone_number, client.email,
            client.vat_pan, client.nid_citizen, client.passport_number,
            client.company_name, client.unique_id,
            client.agent.email if client.agent else '',
            client.billed_by.email if client.billed_by else '',
            client.created_by.email if client.created_by else '',
            addr.city if addr else '', addr.province if addr else '', addr.district if addr else '',
            addr.ward_no if addr else '', addr.street_name if addr else '',
            paddr.city if paddr else '', paddr.province if paddr else '', paddr.district if paddr else '',
            paddr.ward_no if paddr else '', paddr.street_name if paddr else ''
        ])

    return response
