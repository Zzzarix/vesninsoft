from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    name = models.CharField('Название', null=False, max_length=500)
    inn = models.BigIntegerField('ИНН', primary_key=True)
    kpp = models.BigIntegerField('КПП')

    def __str__(self) -> str:
        return f"<Company {self.name} {self.inn}>"

    class Meta:
        ordering = ['name', 'inn']
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class User(AbstractUser):
    phone = models.CharField('Телефон', max_length=12, unique=True, null=True)
    password = models.CharField('Пароль', max_length=128, null=False)
    first_name = models.CharField('Имя', max_length=50, null=True)
    patronymic = models.CharField('Отчество', max_length=50, null=True)
    last_name = models.CharField('Фамилия', max_length=50, null=True)
    snils = models.CharField('СНИЛС', unique=True, null=False, max_length=11)

    is_corporative = models.BooleanField('Корпоративный пользователь', default=False)

    USERNAME_FIELD = 'phone'

    def __str__(self) -> str:
        if self.is_corporative:
            return f"<CorporativeUser {self.corporative_username} {self.company.name}>"
        return f"<User {self.phone} {self.first_name} {self.patronymic} {self.last_name}>"

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

User.check_password


# class Document(models.Model):

#     def __str__(self) -> str:
#         return f"<Document {self.phone}>"

#     class Meta:
#         ordering = ['company']
#         verbose_name = 'Документ'
#         verbose_name_plural = 'Документы'


class PayslipRegistry(models.Model):
    id = models.BigAutoField('Идентификатор', primary_key=True)
    company = models.ForeignKey(Company, related_name='Организация', max_length=50, on_delete=models.CASCADE)
    month = models.IntegerField('Месяц начисления')
    year = models.IntegerField('Год начисления')
    inn = models.BigIntegerField('ИНН')

    def __str__(self) -> str:
        return f"<PayslipRegistry {self.company} {self.month}.{self.year}>"

    class Meta:
        ordering = ['id', 'company']
        verbose_name = 'Реестр рассчётных листов'
        verbose_name_plural = 'Реестры рассчётных листов'


class PayslipSheet(models.Model):
    id = models.BigAutoField('Идентификатор', primary_key=True)
    registry = models.ForeignKey(PayslipRegistry, related_name='Реестр', on_delete=models.CASCADE)
    number = models.IntegerField('Номер листа')

    full_name = models.CharField('ФИО', max_length=120)
    bank_number = models.CharField('Номер Лицевого Счета', max_length=20)
    subdivision = models.CharField('Подразделение', max_length=100)
    specialization = models.CharField('Должность', max_length=100)

    accruals = models.JSONField('Начисления', default=dict)

    # accrual_salary = models.DecimalField('Оклад')
    # accrual_salary_description = models.CharField(
    #     'Оклад описание начисления', max_length=150)

    # accrual_regional_coefficient = models.DecimalField(
    #     'Региональный коеффициент')
    # accrual_regional_coefficient_description = models.CharField(
    #     'Региональный коеффициент описание начисления', max_length=150)

    # accrual_allowances = models.DecimalField('Северные надбавки')
    # accrual_allowances_description = models.CharField(
    #     'Северные надбавки описание начисления', max_length=150)


    holds = models.JSONField('Удержания', default=dict)
    
    # holds = models.DecimalField('Удержания')
    

    # holds_tax = models.DecimalField('Налог на доходы')
    # holds_tax_description = models.CharField(
    #     'Налог на доходы описание удержания', max_length=150)

    # payments = models.DecimalField('Выплаты')

    # payments_salary = models.DecimalField('Перечисление зарплаты')
    # payments_salary_description = models.CharField(
    #     'Перечисление зарплаты описание выплаты', max_length=150)


    info = models.JSONField('Справочная информация', default=dict)

    # info_days_worked = models.DecimalField('Отработано дней')
    # info_hours_worked = models.DecimalField('Отработано часов')
    # info_salary = models.DecimalField('Размер оклада')
    # info_remainder = models.DecimalField('Остаток на начало')
    # info_sum = models.DecimalField('Отработано дней')

    def __str__(self) -> str:
        return f"<PayslipSheet {self.registry.id} {self.number}>"

    class Meta:
        ordering = ['id', 'registry']
        verbose_name = 'Рассчётный лист'
        verbose_name_plural = 'Рассчётные листы'


# class Employee(models.Model):
#     id = models.BigAutoField('Идентификатор', primary_key=True)
#     sheet = models.ForeignKey(PayslipSheet, 'Лист', on_delete=models.CASCADE)
#     full_name = models.CharField('ФИО', max_length=120)
#     bank_number = models.CharField('Номер Лицевого Счета', max_length=20)
#     subdivision = models.CharField('Подразделение', max_length=100)
#     specialization = models.CharField('Должность', max_length=100)

#     def __str__(self) -> str:
#         return f"<PayslipRegistry {self.company} {self.month}.{self.year}>"

#     class Meta:
#         ordering = ['id', 'full_name']
#         verbose_name = 'Сотрудник'
#         verbose_name_plural = 'Сотрудники'
