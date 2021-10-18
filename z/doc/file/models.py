from django.db import models
from z.saas.models import Account
from django.contrib.auth.models import User
from z.meta.abstract.models import TrackedOwnedModel
import magic

def upload_docs_to(inst, filename):
    return os.path.join(settings.ACCOUNT_DATA_ROOT, inst.account.login, 'docs', filename)

class DocFile(TrackedOwnedModel):	
    title = models.CharField(max_length=100)
    doc = models.FileField(upload_to=upload_docs_to)
    description = models.TextField(blank=True, default="")
    filetype = models.CharField(max_length=100, blank=True, default="")

    def save(self):
        m = magic.Magic()
        super(DocFile, self).save()
        self.filetype = m.from_file(self.doc.path)
        super(DocFile, self).save()

    @property
    def human_size(self):
        if self.doc.size > pow(1024, 3):
            return "%.2f GB" %(float(self.doc.size) / pow(1024, 3))
        elif self.doc.size > pow(1024, 2):
            return "%.2f MB" %(float(self.doc.size) / pow(1024, 2))
        elif self.doc.size > 1024:
            return "%.2f KB" %(float(self.doc.size) / 1024)
#            return "%f KB" %(round(float(self.doc.size) / 1024), 2)
        else:
            return "%f" %(self.doc.size)

    @property
    def short_type(self):
        if len(self.filetype) > 30:
            return self.filetype[:30] + "..."
        return self.filetype
