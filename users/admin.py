from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User, Team
class UserAdmin(BaseUserAdmin):
	fieldsets = (
		(None, {'fields': ('email', 'password', )}),
		(('Personal info'), {'fields': ('username',)}),
		(('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
										'groups', 'user_permissions')}),
		(('Important dates'), {'fields': ('last_login', 'date_joined')}),
			(('user_info'), {'fields': ('is_team_leader', 'is_team_member')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide', ),
			'fields': ('email','username','is_team_leader', 'is_team_member', 'password1', 'password2'),
		}),
	)
	list_display = ['email', 'first_name', 'last_name', 'is_staff', "is_team_member", "is_team_leader"]
	search_fields = ('email', 'first_name', 'last_name')
	ordering = ('email', )
admin.site.register(User, UserAdmin)

admin.site.register(Team)
