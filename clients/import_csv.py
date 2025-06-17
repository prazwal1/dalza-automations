from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils.dateparse import parse_date
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages
from io import TextIOWrapper
import csv
from user_authen.models import CustomUser
from .models import *
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def import_clients_csv(request):
    if request.method != 'POST' or 'file' not in request.FILES:
        messages.error(request, 'No file uploaded or invalid request method.')
        return redirect('client_list')

    file = request.FILES['file']
    
    # Validate file type
    if not file.name.endswith('.csv'):
        messages.error(request, 'Please upload a CSV file.')
        return redirect('client_list')

    # Better file handling
    try:
        # Decode the file content
        file_content = file.read().decode('utf-8')
        file.seek(0)  # Reset file pointer
        
        # Use StringIO for better CSV handling
        from io import StringIO
        csv_file = StringIO(file_content)
        reader = csv.DictReader(csv_file)
        
        success_count = 0
        error_count = 0
        errors = []

        with transaction.atomic():
            for i, row in enumerate(reader, start=1):
                try:
                    # Log the row being processed
                    logger.info(f"Processing row {i}: {row}")
                    
                    # Validate required fields
                    if not row.get('first_name') or not row.get('last_name'):
                        error_msg = f"Row {i}: Missing required fields (first_name or last_name)"
                        errors.append(error_msg)
                        logger.warning(error_msg)
                        error_count += 1
                        continue

                    client_data = {
                        'first_name': row.get('first_name', '').strip(),
                        'last_name': row.get('last_name', '').strip(),
                        'dob': parse_date(row.get('dob')) if row.get('dob') else None,
                        'gender': row.get('gender', '').strip(),
                        'nationality': row.get('nationality', '').strip(),
                        'address': row.get('address', '').strip(),
                        'city': row.get('city', '').strip(),
                        'province': row.get('province', '').strip(),
                        'zip': row.get('zip', '').strip(),
                        'country': row.get('country', '').strip(),
                        'perma_address': row.get('perma_address', '').strip(),
                        'phone_number': row.get('phone_number', '').strip(),
                        'email': row.get('email', '').strip(),
                        'vat_pan': row.get('vat_pan', '').strip(),
                        'nid_citizen': row.get('nid_citizen', '').strip(),
                        'passport_number': row.get('passport_number', '').strip(),
                        'company_name': row.get('company_name', '').strip(),
                        'unique_id': row.get('unique_id', '').strip(),
                    }

                    # Handle foreign key relationships with better error handling
                    
                    agent = request.user
                    billed_by = request.user
                    created_by = request.user

                    
                    # Use appropriate field for user lookup - try name, email, or id
                    if row.get('agent'):
                        try:
                            # Try to find by name first, then email, then id
                            agent_identifier = row.get('agent')
                            if agent_identifier.isdigit():
                                agent = CustomUser.objects.get(id=agent_identifier)
                            elif '@' in agent_identifier:
                                agent = CustomUser.objects.get(email=agent_identifier)
                            else:
                                agent = CustomUser.objects.get(name=agent_identifier)
                        except CustomUser.DoesNotExist:
                            logger.warning(f"Row {i}: Agent '{row.get('agent')}' not found")
                        except CustomUser.MultipleObjectsReturned:
                            logger.warning(f"Row {i}: Multiple agents found for '{row.get('agent')}'")
                    
                    if row.get('billed_by'):
                        try:
                            billed_by_identifier = row.get('billed_by')
                            if billed_by_identifier.isdigit():
                                billed_by = CustomUser.objects.get(id=billed_by_identifier)
                            elif '@' in billed_by_identifier:
                                billed_by = CustomUser.objects.get(email=billed_by_identifier)
                            else:
                                billed_by = CustomUser.objects.get(name=billed_by_identifier)
                        except CustomUser.DoesNotExist:
                            logger.warning(f"Row {i}: Billed_by user '{row.get('billed_by')}' not found")
                        except CustomUser.MultipleObjectsReturned:
                            logger.warning(f"Row {i}: Multiple users found for billed_by '{row.get('billed_by')}'")
                    
                    if row.get('created_by'):
                        try:
                            created_by_identifier = row.get('created_by')
                            if created_by_identifier.isdigit():
                                created_by = CustomUser.objects.get(id=created_by_identifier)
                            elif '@' in created_by_identifier:
                                created_by = CustomUser.objects.get(email=created_by_identifier)
                            else:
                                created_by = CustomUser.objects.get(name=created_by_identifier)
                        except CustomUser.DoesNotExist:
                            logger.warning(f"Row {i}: Created_by user '{row.get('created_by')}' not found")
                        except CustomUser.MultipleObjectsReturned:
                            logger.warning(f"Row {i}: Multiple users found for created_by '{row.get('created_by')}')")

                    # Create client
                    client = Client.objects.create(
                        agent=agent,
                        billed_by=billed_by,
                        created_by=created_by,
                        **client_data
                    )
                    logger.info(f"Created client: {client.first_name} {client.last_name}")

                    # InternetDetails
                    if row.get('username_or_mac'):
                        service_plan = None
                        user_group = None
                        
                        if row.get('service_plan'):
                            try:
                                service_plan = ServicePlan.objects.get(name=row.get('service_plan'))
                            except ServicePlan.DoesNotExist:
                                logger.warning(f"Row {i}: Service plan '{row.get('service_plan')}' not found")
                        
                        if row.get('user_group'):
                            try:
                                user_group = UserGroup.objects.get(name=row.get('user_group'))
                            except UserGroup.DoesNotExist:
                                logger.warning(f"Row {i}: User group '{row.get('user_group')}' not found")

                        # Safe integer conversion
                        def safe_int(value, default=0):
                            try:
                                return int(value) if value else default
                            except (ValueError, TypeError):
                                return default

                        InternetDetails.objects.create(
                            customer=client,
                            username_or_mac=row['username_or_mac'],
                            enable=row.get('enable', 'True').lower() == 'true',
                            mac_user=row.get('mac_user', 'False').lower() == 'true',
                            password=row.get('password', ''),
                            mac_address_of_cm=row.get('mac_address_of_cm', ''),
                            simultaneous_use=safe_int(row.get('simultaneous_use'), 1),
                            service_plan=service_plan,
                            user_group=user_group,
                            download_limit=safe_int(row.get('download_limit'), 0),
                            upload_limit=safe_int(row.get('upload_limit'), 0),
                            total_limit=safe_int(row.get('total_limit'), 0),
                            account_expiry_date=parse_date(row.get('account_expiry_date')) if row.get('account_expiry_date') else None,
                            radius_comments=row.get('radius_comments', ''),
                            radius_attribute=row.get('radius_attribute', '')
                        )

                    # InsuranceDetails
                    if row.get('insurance_comments'):
                        InsuranceDetails.objects.create(
                            customer=client,
                            insurance_comments=row.get('insurance_comments', '')
                        )

                    # TrackingDetails
                    if row.get('travel_from'):
                        TrackingDetails.objects.create(
                            customer=client,
                            travel_from=row['travel_from'],
                            emergency_contact=row.get('emergency_contact', ''),
                            package=row.get('package', ''),
                            travel_start_date=parse_date(row.get('travel_start_date')) if row.get('travel_start_date') else None,
                            travel_end_date=parse_date(row.get('travel_end_date')) if row.get('travel_end_date') else None
                        )

                    success_count += 1

                except Exception as e:
                    error_msg = f"Row {i}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(error_msg, exc_info=True)
                    error_count += 1
                    continue

        # Provide feedback to user
        if success_count > 0:
            messages.success(request, f'Successfully imported {success_count} clients.')
        
        if error_count > 0:
            messages.warning(request, f'{error_count} rows had errors and were skipped.')
            # Optionally log first few errors for debugging
            for error in errors[:5]:  # Show first 5 errors
                messages.error(request, error)

    except Exception as e:
        logger.error(f"File processing error: {str(e)}", exc_info=True)
        messages.error(request, f'File processing error: {str(e)}')

    return redirect('client_list')