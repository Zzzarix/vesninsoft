from xml.dom import minidom
from account.models import PayslipRegistry, PayslipSheet, Company, User, CompanyAdmin
from django.contrib.auth.hashers import make_password
from enum import Enum

PATH = r'D:\Downloads\xml_payslips.xml'

def parse_payslip_registry(content: str | bytes):

    ENCODING = 'utf-8'  # 'windows-1251'

    data: minidom.Document = minidom.parseString(content)

    for _registry in data.getElementsByTagName('РеестрРасчетныхЛистов'):
        _registry: minidom.Element
        company, _ = Company.objects.get_or_create(inn=_registry.getAttribute('ИНН'), name=_registry.getAttribute('Организация'))
        registry, _ = PayslipRegistry.objects.get_or_create(company=company, month=_registry.getAttribute('ПериодНачисленияМесяц'), year=_registry.getAttribute('ПериодНачисленияГод'))
    
        for _sheet in _registry.getElementsByTagName('РасчетныйЛист'):
            _sheet: minidom.Element
            _sheet.childNodes
            _employee: minidom.Element = _sheet.getElementsByTagName('Сотрудник')[0]

            sheet_flag = PayslipSheet.objects.filter(registry=registry.id, number=_sheet.getAttribute('Нпп')).exists()

            if not sheet_flag:
                full_name = _employee.getElementsByTagName('ФИО')[0].childNodes[0].nodeValue
                phone = _employee.getElementsByTagName('Телефон')[0].childNodes[0].nodeValue
                
                if not phone.startswith('+7'):
                    phone = phone.replace('8', '+7', 1).replace(' ', '').replace('-', '')[:12]
                
                snils = _employee.getElementsByTagName('СНИЛС')[0].childNodes[0].nodeValue
                subdivision = _employee.getElementsByTagName('Подразделение')[0].childNodes[0].nodeValue
                specialization = _employee.getElementsByTagName('Должность')[0].childNodes[0].nodeValue

                try:
                    user = User.objects.get(phone=phone)
                    if not user.snils:
                        user.snils = snils
                        user.save()
                except:
                    pass

                def __parse_sheet(category: minidom.Element) -> dict:
                    result = {}
                    if category.getAttribute('Всего'):
                        result['Всего'] = {
                                'Всего': category.getAttribute('Всего')
                        }

                    for child in category.childNodes:
                        if not isinstance(child, minidom.Element):
                            continue
                        
                        items = list(child.attributes.items())
                        kind = items[0][1]
                        for k, v in items[1:]:
                            result[kind] = {
                                k: v
                                # 'Описание': child.getAttribute('Описание'),
                                # 'Сумма': child.getAttribute('Сумма'),
                            }
                    return result

                accruals = __parse_sheet(_sheet.getElementsByTagName('Начисления')[0])
                holds = __parse_sheet(_sheet.getElementsByTagName('Удержания')[0])
                payments = __parse_sheet(_sheet.getElementsByTagName('Выплаты')[0])
                info = __parse_sheet(_sheet.getElementsByTagName('Справочно')[0])

                PayslipSheet.objects.create(registry=registry, number=_sheet.getAttribute('Нпп'), full_name=full_name, phone=phone, snils=snils, subdivision=subdivision, specialization=specialization, accruals=accruals, holds=holds, payments=payments, info=info)


class AddOrgStatus(Enum):
    INCORRECT_USER = 0
    ALREADY_LINKED_OTHER_COMPANY = 1
    OK = 2


def parse_org(content: str | bytes) -> AddOrgStatus:

    ENCODING = 'utf-8'  # 'windows-1251'

    data: minidom.Document = minidom.parseString(content)

    for _org in data.getElementsByTagName('Организация'):
        _org: minidom.Element
        admin_username = _org.getAttribute('Имя пользователя')
        admin_password = make_password(_org.getAttribute('Пароль пользователя'))

        inn = _org.getAttribute('ИНН')
        name = _org.getAttribute('Организация')
        kpp = _org.getAttribute('КПП')
        try:
            admin = CompanyAdmin.objects.get(username=admin_username, password=admin_password)
            if admin.company:
                if not inn == admin.company.inn:
                    return AddOrgStatus.ALREADY_LINKED_OTHER_COMPANY
            company = Company.objects.get_or_create(inn=inn, name=name, kpp=kpp)
            admin.company = company
            admin.save()
            return AddOrgStatus.OK
        except Exception:
            return AddOrgStatus.INCORRECT_USER
