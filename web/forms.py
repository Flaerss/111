from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField,
    TextAreaField,
    SelectField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired, 
    Length, 
    EqualTo,
    ValidationError
)
from web.models import Admin

# Форма для работы с шаблонами сообщений
class TemplateForm(FlaskForm):
    TRIGGER_CHOICES = [
        ('booking_create', 'Новая запись'),
        ('booking_update', 'Изменение записи'),
        ('booking_delete', 'Отмена записи'),
        ('24h_reminder', 'Напоминание за 24 часа'),
        ('1h_reminder', 'Напоминание за 1 час')
    ]
    
    PLATFORM_CHOICES = [
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp')
    ]

    name = StringField('Название шаблона', validators=[
        DataRequired(message="Обязательное поле"),
        Length(max=50)
    ])
    
    content = TextAreaField('Текст сообщения', validators=[
        DataRequired(message="Введите текст шаблона")
    ])
    
    trigger_event = SelectField('Тип события', 
        choices=TRIGGER_CHOICES,
        validators=[DataRequired()]
    )
    
    platform = SelectField('Платформа',
        choices=PLATFORM_CHOICES,
        validators=[DataRequired()]
    )
    
    is_active = BooleanField('Активен')
    
    submit = SubmitField('Сохранить')

# Форма для создания/редактирования администраторов
class AdminForm(FlaskForm):
    username = StringField('Логин', validators=[
        DataRequired(),
        Length(min=3, max=100)
    ])
    
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6),
        EqualTo('confirm_password', message='Пароли должны совпадать')
    ])
    
    confirm_password = PasswordField('Подтвердите пароль')
    
    submit = SubmitField('Создать аккаунт')

    def validate_username(self, username):
        admin = Admin.query.filter_by(username=username.data).first()
        if admin:
            raise ValidationError('Этот логин уже занят')

# Форма поиска клиентов
class ClientSearchForm(FlaskForm):
    search_query = StringField('Поиск клиента', validators=[
        Length(max=50)
    ])
    
    submit = SubmitField('Найти')