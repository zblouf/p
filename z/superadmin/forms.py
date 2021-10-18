from django import forms
from z.retail.vendor.models import Vendor

ACCOUNT_TYPES = (
                ("START", "Start"),
                ("STANDARD", "Standard"),
                ("PRO", "Pro"),
                )

class CreateAccountForm(forms.Form):
	account_name = forms.CharField(max_length=100, label="Nom", help_text="Nom complet du compte")
	account_slug = forms.SlugField(label="Identifiant", help_text="Identifiant du compte, comprenant uniquement lettres, chiffres et underscore (_)")
	account_type = forms.ChoiceField(choices=ACCOUNT_TYPES)
	account_vendor = forms.ModelChoiceField(queryset=Vendor.objects.all())

	admin_login = forms.CharField(max_length=100, label="Identifiant administrateur")
	admin_email = forms.EmailField(max_length=100, label="e-Mail administrateur")
	admin_pass = forms.CharField(max_length=100, label="Mot de passe administrateur")
	admin_pass_confirm = forms.CharField(max_length=100, label="Confirmation mot de passe")


class CreateRetailerForm(forms.Form):
	retailer_name = forms.CharField(max_length=100, label="Nom", help_text="Nom complet du compte")
	retailer_slug = forms.SlugField(label="Identifiant", help_text="Identifiant du compte, comprenant uniquement lettres, chiffres et underscore (_)")
	retailer_type = forms.ChoiceField(choices=ACCOUNT_TYPES)

