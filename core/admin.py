from django.contrib import admin
from .models import UserWallet, DepositRequest

# የአድሚን ርዕስ መቀየሪያ
admin.site.site_header = 'Administration'
admin.site.site_title = 'Administration'
admin.site.index_title = 'Administration Control Panel'

admin.site.register(UserWallet)

@admin.register(DepositRequest)
class DepositRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'created_at']
    list_filter = ['status']
    actions = ['approve_deposit', 'reject_deposit']

    def approve_deposit(self, request, queryset):
        for obj in queryset:
            if obj.status == 'Pending':
                obj.status = 'Approved'
                obj.save()

                # የተጠቃሚውን ዋሌት አግኝቶ ብሩን መደመር
                wallet = UserWallet.objects.get(user=obj.user)
                wallet.balance += obj.amount
                wallet.save()

        self.message_user(request, "የተመረጡት ክፍያዎች ጸድቀዋል፣ ብሩም ለተጠቃሚዎቹ ገብቷል!")

    approve_deposit.short_description = "የተመረጡትን ክፍያዎች አጽድቅ (ገንዘብ ጨምር)"

    def reject_deposit(self, request, queryset):
        queryset.update(status='Rejected')

    reject_deposit.short_description = "የተመረጡትን ክፍያዎች ሰርዝ"