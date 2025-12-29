"""
Management command to create sample institutions, colleges, and departments.
Run with: python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from admin_panel.models import Institution, College, Department


class Command(BaseCommand):
    help = 'Create sample institutions, colleges, and departments'
    
    def handle(self, *args, **options):
        """Create sample data"""
        
        # Create Institutions
        institutions_data = [
            {
                'institution_name': 'Anna University',
                'institution_code': 'ANNA',
                'institution_email': 'admin@annauniv.edu.in',
                'institution_phone': '044-12345678',
                'address': 'Chennai'
            },
            {
                'institution_name': 'Madras University',
                'institution_code': 'MADRAS',
                'institution_email': 'admin@madrasuniv.edu.in',
                'institution_phone': '044-87654321',
                'address': 'Guindy, Chennai'
            },
            {
                'institution_name': 'SASTRA University',
                'institution_code': 'SASTRA',
                'institution_email': 'admin@sastra.edu.in',
                'institution_phone': '04362-264101',
                'address': 'Thanjavur'
            }
        ]
        
        institutions = {}
        for inst_data in institutions_data:
            inst, created = Institution.objects.get_or_create(**inst_data)
            institutions[inst.id] = inst
            status = "Created" if created else "Already exists"
            self.stdout.write(self.style.SUCCESS(f'✓ Institution: {inst.institution_name} - {status}'))
        
        # Create Colleges for each institution
        colleges_data = {
            1: [
                {'college_name': 'College of Engineering', 'college_code': 'COE'},
                {'college_name': 'College of Arts', 'college_code': 'COA'},
                {'college_name': 'College of Science', 'college_code': 'COS'},
            ],
            2: [
                {'college_name': 'Engineering College', 'college_code': 'ENG'},
                {'college_name': 'Arts College', 'college_code': 'ART'},
            ],
            3: [
                {'college_name': 'School of Engineering', 'college_code': 'SOE'},
                {'college_name': 'School of Law', 'college_code': 'SOL'},
            ]
        }
        
        colleges = {}
        for inst_id, colleges_list in colleges_data.items():
            institution = Institution.objects.get(id=inst_id)
            for college_data in colleges_list:
                college_data['institution'] = institution
                college, created = College.objects.get_or_create(
                    college_name=college_data['college_name'],
                    institution=institution,
                    defaults={'college_code': college_data['college_code']}
                )
                colleges[college.id] = college
                status = "Created" if created else "Already exists"
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ College: {college.college_name} ({institution.institution_name}) - {status}'
                    )
                )
        
        # Create Departments for each college
        departments_data = {
            1: [  # College of Engineering
                {'department_name': 'Computer Science', 'department_code': 'CSE'},
                {'department_name': 'Electrical Engineering', 'department_code': 'EEE'},
                {'department_name': 'Mechanical Engineering', 'department_code': 'MECH'},
                {'department_name': 'Civil Engineering', 'department_code': 'CIVIL'},
            ],
            2: [  # College of Arts
                {'department_name': 'English', 'department_code': 'ENG'},
                {'department_name': 'Tamil', 'department_code': 'TAM'},
                {'department_name': 'History', 'department_code': 'HIST'},
            ],
            3: [  # College of Science
                {'department_name': 'Physics', 'department_code': 'PHY'},
                {'department_name': 'Chemistry', 'department_code': 'CHEM'},
                {'department_name': 'Botany', 'department_code': 'BOT'},
            ],
            4: [  # Engineering College (Madras Univ)
                {'department_name': 'Computer Science', 'department_code': 'CSE'},
                {'department_name': 'Electronics', 'department_code': 'ECE'},
            ],
            5: [  # Arts College (Madras Univ)
                {'department_name': 'Economics', 'department_code': 'ECO'},
                {'department_name': 'Political Science', 'department_code': 'POLI'},
            ],
            6: [  # School of Engineering (SASTRA)
                {'department_name': 'Computer Science', 'department_code': 'CSE'},
                {'department_name': 'Information Technology', 'department_code': 'IT'},
            ],
            7: [  # School of Law (SASTRA)
                {'department_name': 'Constitutional Law', 'department_code': 'CON'},
                {'department_name': 'Criminal Law', 'department_code': 'CRIM'},
            ]
        }
        
        for college_id, departments_list in departments_data.items():
            college = College.objects.get(id=college_id)
            for dept_data in departments_list:
                dept, created = Department.objects.get_or_create(
                    department_name=dept_data['department_name'],
                    college=college,
                    defaults={
                        'department_code': dept_data['department_code'],
                        'institution': college.institution
                    }
                )
                status = "Created" if created else "Already exists"
                self.stdout.write(
                    self.style.SUCCESS(
                        f'    ✓ Department: {dept.department_name} ({dept.department_code}) - {status}'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sample data creation completed!'))
        
        # Print summary
        self.stdout.write('\n' + self.style.WARNING('=== Summary ==='))
        self.stdout.write(f'Institutions: {Institution.objects.count()}')
        self.stdout.write(f'Colleges: {College.objects.count()}')
        self.stdout.write(f'Departments: {Department.objects.count()}')
        self.stdout.write('\n' + self.style.WARNING('=== Next Steps ==='))
        self.stdout.write('1. Create users (HOD, HR, Admin) with these institutions/colleges/departments')
        self.stdout.write('2. Login with admin credentials')
        self.stdout.write('3. Assign users to institutions and departments')
