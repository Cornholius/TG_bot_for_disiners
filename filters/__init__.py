from .is_admin import IsAdmin
from loader import dp


dp.filters_factory.bind(IsAdmin)
